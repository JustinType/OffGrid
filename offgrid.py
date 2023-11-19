from pyudev import Context, Monitor, MonitorObserver
from threading import Thread, Lock, Event
from docker.errors import NotFound
import xml.etree.ElementTree as ET
from hashlib import sha256
import requests.exceptions
from time import sleep
import subprocess
import threading
import logging
import signal
import docker
import re
import os

# Ce service doit tourner en continu pour écouter les signaux UDEV venant du branchement d'un périphérique USB et
# fournir les informations des périphériques à VolWeb.

DOCKER_COMPOSE_FILE = "./docker/docker-compose.yml"
COMPOSE_VERSION = "3"
STACK_NAME = "volweb"
TIMEOUT = 60

LOG_FILE_PATH = "./offgrid.log"

AVAILABLE_DEVICES_NODE = {}
# Le fichier XML contenant les périphériques disponibles pour le service web
AVAILABLE_DEVICES_XML_FILE_PATH = "./docker/shared-folder/xml/available_devices.xml"
# Le fichier XML contenant les requêtes du service web
DEVICE_REQUESTS_XML_FILE_PATH = "./docker/shared-folder/xml/device_requests.xml"
MOUNT_POINT_ROOT = "./mount-points"
CONTAINER_MOUNT_POINT_ROOT = "django:/home/app/web/temp"

UUID_SEED = "ID_PART_TABLE_UUID"
BACKUP_UUID_SEED = "ID_FS_UUID"

def ignore_interrupt(signal, frame):
    pass

class Watcher:
    def __init__(self):
        # Parametrage de pyudev, pour écouter les signaux UDEV venant du branchement d'un périphérique USB
        self.context = Context()
        self.stop_event = Event()
        self.monitor = Monitor.from_netlink(self.context)
        self.monitor.filter_by(subsystem='block')
        # Lorsqu'un event UDEV pour le sous-système USB arrive, une méthode pour connecter le périphérique est exécutée
        self.observer = MonitorObserver(self.monitor, callback=manage_device)

    def start(self):
        if get_docker_stack_status() == 0:
            # La stack n'est pas déployée, on la démarre.
            logging.info(f"Démarrage de la stack {STACK_NAME}... (délai maximum : {TIMEOUT} secondes)")
            try:
                subprocess.run(["docker", "compose", "-f", DOCKER_COMPOSE_FILE, "up", "--build", "-d"], check=True)
            except subprocess.CalledProcessError as error:
                logging.critical(f"Une erreur s'est produite lors du déploiement de la stack : {error}")
                exit(1)

        # On attend que le domaine soit en marche.
        for i in range(TIMEOUT):
            if get_docker_stack_status() == 1:
                break

            if i == TIMEOUT - 1:
                logging.critical(f"La stack {STACK_NAME} n'a pas démarré dans les temps.")
                exit(1)
            sleep(1)

        menu.start()

        self.observer.start()
        logging.info("Service de gestion des périphériques USB démarré.")
        while get_docker_stack_status() == 1 and not self.stop_event.is_set():
            sleep(1)
        logging.info("La stack a été arrêtée. Arrêt du service de gestion des périphériques USB.")
        self.observer.send_stop()
        reset_xml_file(AVAILABLE_DEVICES_XML_FILE_PATH)
        reset_xml_file(DEVICE_REQUESTS_XML_FILE_PATH)
        xml_reader.stop_event.set()

    def stop(self):
        logging.info(f"Arrêt de la stack {STACK_NAME}... (délai maximum : {TIMEOUT} secondes)")
        try:
            subprocess.run(["docker", "compose", "-f", DOCKER_COMPOSE_FILE, "down", "--remove-orphans", "--volumes", "--timeout", "0"], check=True)
        except subprocess.CalledProcessError as error:
            logging.critical(f"Une erreur s'est produite lors de l'arrêt de la stack : {error}")


def get_docker_stack_status():
    client = docker.from_env()

    for i in range(10):
        try:
            # Tant que la commande fait un timeout, on réessaye.
            stack = client.containers.list(filters={"label": f"com.docker.compose.project={STACK_NAME}"})
        except NotFound:
            # La stack n'est pas déployée.
            return 0
        except requests.exceptions.ReadTimeout:
            continue
        else:
            break

    if not stack:
        # La stack n'est pas déployée.
        return 0
    else:
        all_running = True
        for container in stack:
            container_status = container.status
            if container_status != "running":
                # Un conteneur n'est pas en cours d'exécution.
                all_running = False

        if all_running:
            # La stack est bien déployée et tous les conteneurs sont en cours d'exécution.
            return 1
        else:
            # La stack est déployée, mais certains conteneurs ne sont pas en cours d'exécution.
            return 2


def manage_device(device):
    node = device.device_node
    system_name = device.sys_name

    # Vérification que le périphérique est bien un périphérique de stockage.
    if node is None or not re.match(r'^sd[a-z]$', system_name):
        return

    # Vérification que le périphérique a un système de fichier avec un UUID.
    device_serial_id = device.get(UUID_SEED) or device.get(BACKUP_UUID_SEED)
    if device_serial_id is None:
        logging.warning("Le périphérique ne semble pas avoir de numéro de série. Il ne sera pas traité par sécurité.")
        return

    # Récupération du nom du fabricant du périphérique.
    usb_device_vendor = device.find_parent(subsystem='usb').get('ID_VENDOR_FROM_DATABASE')
    if usb_device_vendor is None:
        usb_device_vendor = device.get('ID_FS_LABEL')

    # On génère un identifiant unique SHA256 pour le périphérique.
    device_serial_id_sha256 = sha256(device_serial_id.encode('utf-8')).hexdigest()

    # Si l'action est 'add', on ajoute le périphérique à la liste des périphériques disponibles.
    if device.action == 'add':
        AVAILABLE_DEVICES_NODE[device_serial_id_sha256] = node
        AVAILABLE_DEVICES_NODE[node] = device_serial_id_sha256
        add_device_to_xml(device_serial_id_sha256, usb_device_vendor)
        logging.info(f"Un périphérique a été ajouté.")
    # Si l'action est 'remove', on retire le périphérique de la liste des périphériques disponibles.
    elif device.action == 'remove':
        try :
            AVAILABLE_DEVICES_NODE.pop(device_serial_id_sha256)
            AVAILABLE_DEVICES_NODE.pop(node)
        except KeyError:
            logging.warning("Un périphérique a été retiré, mais il n'était pas dans la liste des périphériques disponibles.")
        remove_device_from_xml(device_serial_id_sha256)
        logging.info(f"Un périphérique a été retiré.")


def get_root_and_tree_from_xml_file(xml_file_path):
    try:
        with open(xml_file_path, 'r') as xml_file:
            try:
                tree = ET.parse(xml_file)
                root = tree.getroot()
            except ET.ParseError:
                logging.warning("Le fichier XML est invalide. Création d'un nouveau fichier XML.")
                root = ET.Element("devices")
                tree = ET.ElementTree(root)
    except FileNotFoundError:
        with open(xml_file_path, 'w') as xml_file:
            xml_file.write("<devices></devices>")
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

    return root, tree

def add_device_to_xml(serial_id_sha256, usb_device_vendor):
    # Vérification que le fichier XML existe, sinon on le crée.
    try:
        with open(AVAILABLE_DEVICES_XML_FILE_PATH, 'r') as xml_file:
            try:
                tree = ET.parse(xml_file)
                root = tree.getroot()
            except ET.ParseError:
                logging.warning("Le fichier XML est invalide. Création d'un nouveau fichier XML.")
                root = ET.Element("devices")
                tree = ET.ElementTree(root)
    except FileNotFoundError:
        with open(AVAILABLE_DEVICES_XML_FILE_PATH, 'w') as xml_file:
            xml_file.write("<devices></devices>")
        tree = ET.parse(AVAILABLE_DEVICES_XML_FILE_PATH)
        root = tree.getroot()

    # Vérification que le périphérique n'est pas déjà présent dans le fichier XML.
    for device in root.findall('device'):
        if device.find('serial_id').text == serial_id_sha256:
            logging.warning("Le périphérique est déjà présent dans le fichier XML. Ceci est un signe de malfonctionnement du "
                  "service de montage des clés USB.")
            return

    # Ajout du périphérique au fichier XML.
    new_device = ET.SubElement(root, 'device')
    ET.SubElement(new_device, 'vendor').text = usb_device_vendor
    ET.SubElement(new_device, 'serial_id').text = serial_id_sha256
    # Ajouter un attribut "mounted" pour savoir si le périphérique est monté ou non. C'est un 0 ou un 1
    ET.SubElement(new_device, 'mounted').text = "0"
    tree.write(AVAILABLE_DEVICES_XML_FILE_PATH)


def update_device_mount_state_in_xml(serial_id_sha256, mounted):
    root, tree = get_root_and_tree_from_xml_file(AVAILABLE_DEVICES_XML_FILE_PATH)
    # Vérification que le périphérique est présent dans le fichier XML.
    for device in root.findall('device'):
        if device.find('serial_id').text == serial_id_sha256:
            device.find('mounted').text = mounted
            tree.write(AVAILABLE_DEVICES_XML_FILE_PATH)
            return

def remove_device_from_xml(serial_id_sha256):
    root, tree = get_root_and_tree_from_xml_file(AVAILABLE_DEVICES_XML_FILE_PATH)
    # Vérification que le périphérique est présent dans le fichier XML.
    for device in root.findall('device'):
        if device.find('serial_id').text == serial_id_sha256:
            root.remove(device)
            tree.write(AVAILABLE_DEVICES_XML_FILE_PATH)
            return


def get_available_devices():
    root, tree = get_root_and_tree_from_xml_file(AVAILABLE_DEVICES_XML_FILE_PATH)
    # Récupération des périphériques disponibles.
    available_devices = {}
    for device in root.findall('device'):
        serial_id = device.find('serial_id').text
        mounted = device.find('mounted').text
        available_devices[serial_id] = mounted

    return available_devices


def get_devices_to_mount():
    root, tree = get_root_and_tree_from_xml_file(DEVICE_REQUESTS_XML_FILE_PATH)
    available_devices = get_available_devices()
    # On récupère les périphériques pour lesquels une demande de montage a été faite.
    devices_to_mount = {}
    for device in root.findall('device'):
        # Si une requête de montage a été faite et que le périphérique est disponible et non monté, on le met dans le dictionnaire.
        if device.find('mount').text == "1":
            if device.find('serial_id').text in available_devices:
                if available_devices[device.find('serial_id').text] == "0":
                    devices_to_mount[AVAILABLE_DEVICES_NODE[device.find('serial_id').text]] = device.find('mount_point').text
    return devices_to_mount


def get_devices_to_umount():
    root, tree = get_root_and_tree_from_xml_file(DEVICE_REQUESTS_XML_FILE_PATH)
    available_devices = get_available_devices()
    # On récupère les périphériques pour lesquels une demande de démontage a été faite.
    devices_to_umount = {}
    for device in root.findall('device'):
        # Si une requête de démontage a été faite et que le périphérique est disponible et monté, on le met dans le dictionnaire.
        if device.find('mount').text == "0":
            if device.find('serial_id').text in available_devices:
                if available_devices[device.find('serial_id').text] == "1":
                    devices_to_umount[AVAILABLE_DEVICES_NODE[device.find('serial_id').text]] = device.find('mount_point').text
    return devices_to_umount

def reset_xml_file(xml_file_path):
    with open(xml_file_path, 'w') as xml_file:
        xml_file.write("<devices></devices>")
    logging.info("Fichier XML " + xml_file_path + " réinitialisé.")


def mount_device(devices_to_mount):
    # on monte les partitions des périphériques.
    for node, mount_point in devices_to_mount.items():
        try:
            subprocess.check_output(["sudo", "umount", node + "1"])
        except subprocess.CalledProcessError:
            pass
        # On essaye de monter les partitions du périphérique.
        try:
            # Creation du point de montage.
            full_mount_point = os.path.join(MOUNT_POINT_ROOT, mount_point)
            if not os.path.exists(full_mount_point):
                os.makedirs(full_mount_point)
            subprocess.check_output(["sudo", "mount", node + "1", os.path.join(MOUNT_POINT_ROOT, mount_point)])
            logging.info("Périphérique " + node + "1" + " monté avec succès.")
            logging.info("Copie des fichiers du périphérique " + node + "1" + " vers le serveur : " + os.path.join(CONTAINER_MOUNT_POINT_ROOT, mount_point))

            # On copie les fichiers du périphérique vers le serveur avec docker cp
            subprocess.check_output(["sudo", "docker", "cp", os.path.join(MOUNT_POINT_ROOT, mount_point), os.path.join(CONTAINER_MOUNT_POINT_ROOT, mount_point)])

            logging.info("Copie des fichiers du périphérique " + node + "1" + " vers le serveur terminée.")

            # On met à jour le fichier XML pour indiquer que le périphérique est monté.
            update_device_mount_state_in_xml(AVAILABLE_DEVICES_NODE[node], "1")
        except subprocess.CalledProcessError:
            logging.warning("Impossible de monter le périphérique " + node + "1" + ".")


def umount_device(devices_to_umount):
    # on démonte les partitions des périphériques.
    for node, mount_point in devices_to_umount.items():
        try:
            full_mount_point = os.path.join(MOUNT_POINT_ROOT, mount_point)
            subprocess.check_output(["sudo", "umount", full_mount_point])
            # Suppression du point de montage.
            if os.path.exists(full_mount_point):
                os.rmdir(full_mount_point)
            logging.info("Périphérique " + node + "1" + " démonté avec succès.")
            # On met à jour le fichier XML pour indiquer que le périphérique est démonté.
            update_device_mount_state_in_xml(AVAILABLE_DEVICES_NODE[node], "0")
        except subprocess.CalledProcessError:
            logging.warning("Impossible de démonter le périphérique " + node + ".")


class XmlReader(threading.Thread):
    def __init__(self):
        super().__init__()
        self.stop_event = Event()

    def run(self):
        while not self.stop_event.is_set():
            devices_to_copy = get_devices_to_mount()
            if devices_to_copy:
                mount_device(devices_to_copy)
                sleep(10)
                umount_device(devices_to_copy)

            sleep(1)


class Menu(threading.Thread):
    def __init__(self):
        super().__init__()
        self.stop_event = Event()

    def run(self):
        while not self.stop_event.is_set():
            print()
            print("1. Lister les périphériques disponibles.")
            print("2. Afficher l'état des containers. (Control + C pour quitter)")
            print("3. Afficher les logs des containers. (Control + C pour quitter)")
            print("4. Afficher les logs du programme de gestion des périphériques.")
            print("5. Quitter.")
            choice = input("Votre choix : ")
            if choice == "1":
                devices = get_available_devices()
                if devices:
                    print("Périphériques disponibles :")
                    for device in devices:
                        print(device)
                else:
                    print("Aucun périphérique disponible.")
            elif choice == "2":
                print("Etat des containers :")
                subprocess.call(["sudo", "docker", "ps", "-a"])
            elif choice == "3":
                print("Logs des containers :")
                subprocess.call(["sudo", "docker", "compose", "-f", DOCKER_COMPOSE_FILE, "logs", "-f"])
            elif choice == "4":
                print("Logs du programme de gestion des périphériques :")
                subprocess.call(["tail", "-f", LOG_FILE_PATH])
            elif choice == "5":
                print("Arrêt du programme...")
                watcher.stop()
                self.stop_event.set()
                watcher.stop_event.set()
                xml_reader.stop_event.set()
            else:
                print("Choix invalide.")


if __name__ == '__main__':
    signal.signal(signal.SIGINT, ignore_interrupt)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename=LOG_FILE_PATH
    )

    reset_xml_file(AVAILABLE_DEVICES_XML_FILE_PATH)
    reset_xml_file(DEVICE_REQUESTS_XML_FILE_PATH)

    devices = {}
    watcher = Watcher()

    xml_reader = XmlReader()
    xml_reader.start()

    menu = Menu()

    watcher.start()

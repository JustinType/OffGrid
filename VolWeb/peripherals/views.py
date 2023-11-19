import uuid
import shutil
from django.contrib.auth.decorators import login_required
from .models import Peripheral
from investigations.models import *
from .forms import PeripheralForm
from django.shortcuts import render, redirect
import xml.etree.ElementTree as ET
from uuid import uuid4
import time
import os

AVAILABLE_DEVICES_XML_FILE_PATH = "./shared-folder/xml/available_devices.xml"
DEVICE_REQUESTS_XML_FILE_PATH = "./shared-folder/xml/device_requests.xml"
MOUNT_TIMEOUT = 600
FILEPATH = "/result/"
DUMP_FILENAME = "memory.raw"
ISF_FILENAME = "memory.json"
CHECKSUM_FILENAME = "memory.sha256"

def get_devices_from_xml(request):
    try:
        with open(AVAILABLE_DEVICES_XML_FILE_PATH, 'r') as xml_file:
            try:
                tree = ET.parse(xml_file)
                root = tree.getroot()
            except ET.ParseError:
                return redirect('Error opening available devices xml file')
    except FileNotFoundError:
        return redirect('Error opening available devices xml file')

    storage_devices = {}
    bash_bunny_devices = {}
    for index, device in enumerate(root.findall('device')):
        serial_id = device.find('serial_id').text
        vendor = device.find('vendor').text
        mounted = device.find('mounted').text

        if vendor == 'BashBunny':
            bash_bunny_devices[index] = {}
            bash_bunny_devices[index]["serial_id"] = serial_id
            bash_bunny_devices[index]["vendor"] = vendor
            bash_bunny_devices[index]["mounted"] = mounted
        else:
            storage_devices[index] = {}
            storage_devices[index]["serial_id"] = serial_id
            storage_devices[index]["vendor"] = vendor
            storage_devices[index]["mounted"] = mounted

    return storage_devices, bash_bunny_devices

@login_required
def new_devices(request):
    """Peripherals dashboard

    Arguments:
    request : http request object

    Comment:
    First entry point to visualize all of the peripherals
    """
    storage_devices, bash_bunny_devices = get_devices_from_xml(request)

    context = {
        'storage_devices': storage_devices,
        'bash_bunny_devices': bash_bunny_devices,
    }

    return render(request, 'peripherals/new-devices.html', context)

@login_required
def register_peripheral(request):
    storage_devices, bash_bunny_devices = get_devices_from_xml(request)

    storage_devices_parsed = []
    for storage_device in storage_devices.values():
        storage_devices_parsed.append(storage_device["vendor"] + " : " + storage_device["serial_id"])

    bash_bunny_devices_parsed = []
    for bash_bunny_device in bash_bunny_devices.values():
        bash_bunny_devices_parsed.append(bash_bunny_device["vendor"] + " : " + bash_bunny_device["serial_id"])

    form = PeripheralForm(bash_bunny_devices=bash_bunny_devices_parsed, storage_devices=storage_devices_parsed)

    if request.method == 'POST':
        print(request.POST)
        form = PeripheralForm(request.POST, bash_bunny_devices=bash_bunny_devices_parsed, storage_devices=storage_devices_parsed)
        if form.is_valid():
            form.save()
            return redirect('peripherals')

    context = {
        'form': form,
    }

    return render(request, 'peripherals/register-peripheral.html', context)



@login_required
def peripherals(request):
    storage_devices, bash_bunny_devices = get_devices_from_xml(request)

    storage_devices_ids = []
    for storage_device in storage_devices.values():
        storage_devices_ids.append(storage_device["serial_id"])
    print("All storage devices: " + str(storage_devices_ids))

    bash_bunny_devices_ids = []
    for bash_bunny_device in bash_bunny_devices.values():
        bash_bunny_devices_ids.append(bash_bunny_device["serial_id"])
    print("All bash bunny devices: " + str(bash_bunny_devices_ids))

    context = {
        "peripherals_dict": {}
    }

    peripherals = Peripheral.objects.all()
    for index, peripheral in enumerate(peripherals):
        context["peripherals_dict"][index] = {}
        context["peripherals_dict"][index]["peripheral"] = peripheral

        if peripheral.storage_device in storage_devices_ids and peripheral.bash_bunny_device in bash_bunny_devices_ids:
            context["peripherals_dict"][index]["available"] = True
        else:
            context["peripherals_dict"][index]["available"] = False

    return render(request, 'peripherals/peripherals.html', context)

@login_required
def auto_investigate(request, storage_device_serial_id):

    mount_point = request_peripheral_mount(storage_device_serial_id)

    peripheral = Peripheral.objects.filter(storage_device=storage_device_serial_id).first()

    if mount_point == None:
        return redirect('Error mounting device')

    print("Fichier copié")
    dump_file_source = "/home/app/web/temp/" + mount_point + FILEPATH + DUMP_FILENAME
    isf_file_source = "/home/app/web/temp/" + mount_point + FILEPATH + ISF_FILENAME
    checksum_file_source = "/home/app/web/temp/" + mount_point + FILEPATH + CHECKSUM_FILENAME

    uid = uuid.uuid4()
    dump_file_destination = str(uid) + "_" + DUMP_FILENAME
    isf_file_destination = str(uid) + "_" + ISF_FILENAME
    checksum_file_destination = str(uid) + "_" + CHECKSUM_FILENAME

    dump_file_destination_path = '/home/app/web/Cases/' + dump_file_destination
    isf_file_destination_path = '/home/app/web/Cases/' + isf_file_destination
    checksum_file_destination_path = '/home/app/web/Cases/' + checksum_file_destination

    print("Déplacement du fichier...")
    shutil.copy2(dump_file_source, dump_file_destination_path)
    shutil.copy2(isf_file_source, isf_file_destination_path)
    shutil.copy2(checksum_file_source, checksum_file_destination_path)
    print("Fichier déplacé")

    print("Création de l'investigation...")
    file_folder = UploadInvestigation()
    file_folder.title = "Invest-" + str(peripheral.name)
    file_folder.os_version = str(peripheral.os_version)
    file_folder.investigators = "user"
    file_folder.description = str(peripheral.description)
    file_folder.status = "0"
    file_folder.percentage = "0"
    file_folder.existingPath = dump_file_destination
    file_folder.eof = "1"
    file_folder.name = dump_file_destination
    file_folder.uid = uid
    file_folder.save()
    print("Investigation créée")

    print("Démontage du périphérique...")
    request_peripheral_umount(storage_device_serial_id)
    print("Périphérique démonté")

    return redirect('investigations')


def request_peripheral_mount(serial_id):
    """Mount a peripheral

    Arguments:
    serial_id : serial id of the peripheral to mount

    Comment:
    Requests the host to mount a peripheral
    """
    try:
        with open(AVAILABLE_DEVICES_XML_FILE_PATH, 'r') as xml_file:
            try:
                tree = ET.parse(xml_file)
                root = tree.getroot()
            except ET.ParseError:
                return redirect('Error opening available devices xml file')
    except FileNotFoundError:
        return redirect('Error opening available devices xml file')

    device_to_mount = None
    for device in root.findall('device'):
        if device.find('serial_id').text == serial_id and device.find('mounted').text == '0':
            device_to_mount = device
            break

    if device_to_mount is None:
        return redirect('Error mounting peripheral')

    print('Mounting device with serial id: ' + serial_id)

    mount_point = str(uuid4())

    try:
        with open(DEVICE_REQUESTS_XML_FILE_PATH, 'r') as xml_file:
            try:
                tree = ET.parse(xml_file)
                root = tree.getroot()
            except ET.ParseError:
                return redirect('Error opening available devices xml file')
    except FileNotFoundError:
        return redirect('Error opening available devices xml file')

    new_device = ET.SubElement(root, 'device')
    ET.SubElement(new_device, 'serial_id').text = serial_id
    ET.SubElement(new_device, 'mount').text = "1"
    ET.SubElement(new_device, 'mount_point').text = mount_point
    tree.write(DEVICE_REQUESTS_XML_FILE_PATH)

    # Wait for the device to be mounted
    for sec in range(MOUNT_TIMEOUT):
        time.sleep(1)
        try:
            with open(AVAILABLE_DEVICES_XML_FILE_PATH, 'r') as xml_file:
                try:
                    tree = ET.parse(xml_file)
                    root = tree.getroot()
                except ET.ParseError:
                    return redirect('Error opening available devices xml file')
        except FileNotFoundError:
            return redirect('Error opening available devices xml file')

        for device in root.findall('device'):
            if device.find('serial_id').text == serial_id and device.find('mounted').text == '1':
                print('Device mounted')
                return mount_point

    return None

def request_peripheral_umount(serial_id):
    """Mount a peripheral

    Arguments:
    serial_id : serial id of the peripheral to umount

    Comment:
    Requests the host to umount a peripheral
    """

    try:
        with open(DEVICE_REQUESTS_XML_FILE_PATH, 'r') as xml_file:
            try:
                tree = ET.parse(xml_file)
                root = tree.getroot()
            except ET.ParseError:
                return redirect('Error opening available devices xml file')
    except FileNotFoundError:
        return redirect('Error opening available devices xml file')

    # find the device to umount
    device_to_umount = None
    for device in root.findall('device'):
        if device.find('serial_id').text == serial_id and device.find('mount').text == '1':
            device_to_umount = device
            break

    if device_to_umount is None:
        return redirect('Error umounting peripheral')

    print('Umounting device with serial id: ' + serial_id)
    device_to_umount.find('mount').text = '0'
    tree.write(DEVICE_REQUESTS_XML_FILE_PATH)

    return
#!/usr/bin/env python3
"""
Script para listar todos los micrófonos disponibles en el sistema
"""

import pyaudio


def list_microphones():
    p = pyaudio.PyAudio()
    print(f"\n{'='*60}")
    print("MICRÓFONOS DISPONIBLES EN TU SISTEMA")
    print(f"{'='*60}\n")

    device_count = p.get_device_count()
    print(f"Total de dispositivos: {device_count}\n")

    for i in range(device_count):
        info = p.get_device_info_by_index(i)
        is_input = info["maxInputChannels"] > 0

        if is_input:
            print(f"[ID: {i}] {info['name']}")
            print(f"    Canales de entrada: {info['maxInputChannels']}")
            print(
                f"    Frecuencia de muestreo: {int(info['defaultSampleRate'])} Hz")
            print()

    p.terminate()


if __name__ == "__main__":
    list_microphones()

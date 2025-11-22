#!/usr/bin/env python3
"""
Script para arreglar imports de openai_chatcompletions -> chatcompletions
"""
import os
import sys

# Archivos a actualizar
files_to_fix = [
    "tools/common.py",
    "tools/reconnaissance/generic_linux_command.py",
    "cli.py",
    "repl/commands/compact.py",
    "repl/commands/flush.py",
    "repl/commands/history.py",
    "repl/commands/load.py",
    "repl/commands/memory.py",
    "repl/commands/parallel.py",
]

# Directorios donde aplicar los cambios
base_dirs = [
    "/home/nipegun/Git/pruebas/CaiFramework",
    "/home/nipegun/PythonVirtualEnvironments/CaiFramework/lib/python3.13/site-packages/cai"
]

old_import = "from cai.sdk.agents.models.openai_chatcompletions import"
new_import = "from cai.sdk.agents.models.chatcompletions import"

def fix_file(filepath):
    """Arregla los imports en un archivo"""
    try:
        with open(filepath, 'r') as f:
            content = f.read()

        if old_import in content:
            new_content = content.replace(old_import, new_import)
            with open(filepath, 'w') as f:
                f.write(new_content)
            print(f"✅ Arreglado: {filepath}")
            return True
        else:
            print(f"⏭️  Sin cambios: {filepath}")
            return False
    except FileNotFoundError:
        print(f"❌ No encontrado: {filepath}")
        return False
    except Exception as e:
        print(f"❌ Error en {filepath}: {e}")
        return False

def main():
    print("🔧 Arreglando imports de openai_chatcompletions -> chatcompletions\n")

    total_fixed = 0
    for base_dir in base_dirs:
        print(f"\n📁 Procesando: {base_dir}")
        print("-" * 60)

        for file_rel in files_to_fix:
            filepath = os.path.join(base_dir, file_rel)
            if fix_file(filepath):
                total_fixed += 1

    print(f"\n✅ Total de archivos arreglados: {total_fixed}")

if __name__ == "__main__":
    main()

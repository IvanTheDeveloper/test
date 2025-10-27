import os
import requests
import argparse

def toggle_variable(var_name: str):
    GH_TOKEN = os.environ.get("GH_TOKEN")
    OWNER = os.environ.get("OWNER")
    REPO = os.environ.get("REPO")

    if not all([GH_TOKEN, OWNER, REPO]):
        raise EnvironmentError("Debe definir GH_TOKEN, OWNER y REPO en el entorno")

    headers = {
        "Authorization": f"Bearer {GH_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    # Obtener valor actual
    url_get = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/variables/{var_name}"
    response = requests.get(url_get, headers=headers)
    response.raise_for_status()
    current_value = response.json().get("value")
    print(f"Valor actual de '{var_name}': {current_value}")

    # Alternar valor
    new_value = "false" if current_value == "true" else "true"
    print(f"Nuevo valor de '{var_name}': {new_value}")

    # Actualizar variable
    url_patch = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/variables/{var_name}"
    data = {"name": var_name, "value": new_value}
    patch_response = requests.patch(url_patch, headers=headers, json=data)
    patch_response.raise_for_status()
    print(f"Variable '{var_name}' actualizada correctamente.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Toggle a GitHub Actions repository variable")
    parser.add_argument("var_name", help="Nombre de la variable a alternar")
    args = parser.parse_args()
    toggle_variable(args.var_name)

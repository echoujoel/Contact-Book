"""A small, persistent command-line contact manager."""

from __future__ import annotations

import json
from pathlib import Path


CONTACTS_FILE = Path(__file__).with_name("contacts.json")


def normalize_name(name: str) -> str:
    """Return a key used for case-insensitive name matching."""
    # Collapse extra spaces and normalize letter case so "Sam Lee" and "sam lee" match.
    return " ".join(name.split()).casefold()


def load_contacts() -> dict[str, dict[str, str]]:
    """Load contacts from disk, keeping each original name and phone number."""
    if not CONTACTS_FILE.exists():
        return {}

    try:
        with CONTACTS_FILE.open("r", encoding="utf-8") as contacts_file:
            saved_contacts = json.load(contacts_file)
    except (OSError, json.JSONDecodeError) as error:
        raise RuntimeError(f"Could not read {CONTACTS_FILE.name}: {error}") from error

    if not isinstance(saved_contacts, list):
        raise RuntimeError(f"{CONTACTS_FILE.name} must contain a JSON list of contacts.")

    # Use normalized names as keys but preserve original names for display.
    contacts: dict[str, dict[str, str]] = {}
    for item in saved_contacts:
        if not isinstance(item, dict):
            continue
        name = item.get("name")
        phone = item.get("phone")
        if isinstance(name, str) and isinstance(phone, str) and name.strip() and phone.strip():
            clean_name = " ".join(name.split())
            contacts[normalize_name(clean_name)] = {"name": clean_name, "phone": phone.strip()}
    return contacts


def save_contacts(contacts: dict[str, dict[str, str]]) -> None:
    """Write contacts to disk in a readable JSON format."""
    # Sort the file for readability and replace it only after the temporary write succeeds.
    saved_contacts = sorted(contacts.values(), key=lambda contact: normalize_name(contact["name"]))
    temporary_file = CONTACTS_FILE.with_suffix(".tmp")
    try:
        with temporary_file.open("w", encoding="utf-8") as contacts_file:
            json.dump(saved_contacts, contacts_file, ensure_ascii=False, indent=2)
            contacts_file.write("\n")
        temporary_file.replace(CONTACTS_FILE)
    except OSError as error:
        try:
            temporary_file.unlink(missing_ok=True)
        except OSError:
            pass
        raise RuntimeError(f"Could not save contacts: {error}") from error


def add_contact(contacts: dict[str, dict[str, str]]) -> None:
    name = " ".join(input("Name: ").split())
    if not name:
        print("A contact name can't be empty.")
        return

    # Check for duplicates before changing the saved data.
    key = normalize_name(name)
    if key in contacts:
        print(f"A contact named {contacts[key]['name']} already exists.")
        return

    phone = input("Phone number: ").strip()
    if not phone:
        print("A phone number can't be empty.")
        return

    contacts[key] = {"name": name, "phone": phone}
    save_contacts(contacts)
    print(f"Added {name}.")


def view_contacts(contacts: dict[str, dict[str, str]]) -> None:
    if not contacts:
        print("No contacts saved yet.")
        return

    print("\nSaved contacts")
    print("-" * 40)
    for contact in sorted(contacts.values(), key=lambda item: normalize_name(item["name"])):
        print(f"{contact['name']:<26} {contact['phone']}")


def search_contact(contacts: dict[str, dict[str, str]]) -> None:
    name = input("Name to search for: ").strip()
    contact = contacts.get(normalize_name(name))
    if contact:
        print(f"{contact['name']}: {contact['phone']}")
    else:
        print(f"No contact named {name or '(blank)'} was found.")


def delete_contact(contacts: dict[str, dict[str, str]]) -> None:
    name = input("Name to delete: ").strip()
    key = normalize_name(name)
    contact = contacts.get(key)
    if not contact:
        print(f"No contact named {name or '(blank)'} was found.")
        return

    # Require an explicit yes so an accidental menu choice cannot remove a contact.
    confirmation = input(f"Delete {contact['name']} ({contact['phone']})? (y/n): ").strip().casefold()
    if confirmation not in {"y", "yes"}:
        print("Deletion cancelled.")
        return

    del contacts[key]
    save_contacts(contacts)
    print(f"Deleted {contact['name']}.")


def print_menu() -> None:
    print("\nContact Manager")
    print("1. Add contact")
    print("2. View contacts")
    print("3. Search contact")
    print("4. Delete contact")
    print("5. Exit")


def main() -> None:
    try:
        contacts = load_contacts()
    except RuntimeError as error:
        print(error)
        return

    # Map menu options to independent functions to keep the main loop simple.
    actions = {
        "1": add_contact,
        "2": view_contacts,
        "3": search_contact,
        "4": delete_contact,
    }

    # Keep showing the menu until the user chooses Exit.
    while True:
        print_menu()
        choice = input("Choose an option (1-5): ").strip()
        if choice == "5":
            print("Goodbye!")
            break

        action = actions.get(choice)
        if action is None:
            print("Please choose a number from 1 to 5.")
            continue

        try:
            action(contacts)
        except RuntimeError as error:
            print(error)


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nGoodbye!")


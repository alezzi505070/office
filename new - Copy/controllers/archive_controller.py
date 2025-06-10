import os
import logging

class ArchiveController:
    """
    Handles dynamic discovery of archive folders based on a template structure and on-disk state.
    """
    def __init__(self, structure, archives_path):
        # structure: nested dict of headers → subheaders → sections → subsections
        self.structure = structure
        self.archives_path = archives_path

    def get_dynamic_folder_options(self, base_folder_path, template_options):
        """
        Returns a sorted list of folder names found both in the template and on disk.

        Args:
            base_folder_path (str): Path on disk to scan.
            template_options (dict|list|None): Template-defined names.

        Returns:
            list[str]: Combined and sorted unique folder names.
        """
        disk_folders = set()
        template_folders = set()

        if os.path.isdir(base_folder_path):
            try:
                for item in os.listdir(base_folder_path):
                    if os.path.isdir(os.path.join(base_folder_path, item)) and not item.startswith('.'):
                        disk_folders.add(item)
            except OSError as e:
                logging.warning(f"Could not scan directory '{base_folder_path}': {e}")
        else:
            logging.debug(f"Base folder path does not exist: {base_folder_path}")

        if isinstance(template_options, dict):
            template_folders = set(template_options.keys())
        elif isinstance(template_options, list):
            template_folders = set(template_options)

        combined = sorted(template_folders.union(disk_folders))
        logging.debug(f"Combined options for '{base_folder_path}': {combined}")
        return combined
import os
from pathlib import Path
from typing import List, Dict, Optional
import random

import napari

from napari_allencell_annotator.view.images_view import ImagesView
from napari_allencell_annotator.model import images_model
from napari_allencell_annotator.constants.constants import SUPPORTED_FILE_TYPES


class ImagesController:
    """
    A Main controller to integrate view and model for image annotations

    Attributes
    ----------
    view
        the GUI and napari viewer

    Methods
    -------
    load_from_csv(files : List[str], shuffled: bool)
        Adds files to file list from a csv list of file paths.

    get_files_dict() -> Dict[str,List[str]]
        Returns the file dictionary that has the current file order.

    is_supported(file_name:str)->bool
        Returns True if a file is a supported file type.

    start_annotating()
        Sets the current item.

    stop_annotating()
        Clears file widget and reset buttons.

    curr_img_dict() -> Dict[str,str]
        Returns a dictionary with the current image attributes.

    next_img()
        Sets the current image to the next in the list.

    prev_img()
        Sets the current image to the previous one in the list.

    get_num_files(self) -> int
        Returns the number of files.
    """

    def __init__(self, viewer: napari.Viewer):
        self.model: images_model = images_model
        self.view: ImagesView = ImagesView(viewer, self)
        self.view.show()
        self._connect_slots()

    def _connect_slots(self):
        """Connects signals to slots."""
        self.view.input_dir.file_selected.connect(self._dir_selected_evt)
        self.view.input_file.file_selected.connect(self._file_selected_evt)
        self.view.shuffle.clicked.connect(self._shuffle_clicked)

    def load_from_csv(self, files: List[str], shuffled: bool):
        """
        Add files to file list from a csv list of file paths.

        If the csv files are shuffled, set shuffle order and hide file names.

        Parameters
        __________
        dct : List[str]
            a list of file paths.
        shuffled: bool
            true if files are shuffled.
        """
        for name in files:
            self.view.file_widget.add_new_item(name, shuffled)
        self.view.disable_csv_image_edits()
        if shuffled:
            self.view.file_widget.set_shuff_order(self.view.file_widget.files_dict)

    def get_files_dict(self) -> (Dict[str, List[str]], bool):
        """
        Return the file dictionary that has the current file order.

        Returns
        ----------
        Dict[str,List[str]], bool
            dictionary of file info. keys in order. a boolean shuffled.
        """
        if self.view.file_widget.shuffled:
            return self.view.file_widget.shuffled_files_dict, True
        else:
            return self.view.file_widget.files_dict, False

    def _shuffle_clicked(self, checked: bool):
        """
        Shuffle file order and hide file names if checked.
        Return files to original order and names if unchecked.

        Side effect: set file_widget.shuffled_files_dict to a new order dict or {} if list is unshuffled.

        Parameters
        ----------
        checked : bool
            Toggle state of the shuffle button.
        """

        files: Dict[str, List[str]] = self.view.file_widget.clear_for_shuff()
        if len(files) > 0:
            if checked:
                self.view.toggle_add(False)
                keys = list(files.keys())
                random.shuffle(keys)
                shuff_dict = {}
                for k in keys:
                    shuff_dict[k] = files[k]
                    self.view.file_widget.add_item(k, hidden=True)
                self.view.file_widget.set_shuff_order(shuff_dict)

            else:
                self.view.toggle_add(True)
                self.view.file_widget.set_shuff_order()
                for f in files.keys():
                    self.view.file_widget.add_item(f, hidden=False)

    @staticmethod
    def is_supported(file_path: str) -> bool:
        """
        Check if the provided file name is a supported file.

        This function checks if the file name extension is in
        the supported file types files.

        Parameters
        ----------
        file_name : str
            Name of the file to check.

        Returns
        -------
        bool
            True if the file is supported.
        """
        if file_path is None:
            return False
        extension = Path(file_path).suffix
        if extension in SUPPORTED_FILE_TYPES:
            return True
        else:
            return False

    def _dir_selected_evt(self, dir_list: List[str]):
        """
        Adds all files in a directory to the GUI.

        Parameters
        ----------
        dir_list : List[str]
            The input list with dir[0] holding directory name.
        """
        if dir_list is not None and len(dir_list) > 0:
            d = dir_list[0]
            if len(os.listdir(d)) < 1:
                self.view.alert("Folder is empty")
            else:
                for file in os.listdir(d):
                    file = d + "/" + file
                    if self.is_supported(file):
                        self.view.file_widget.add_new_item(file)
                    else:
                        self.view.alert("Unsupported file type:" + file)
        else:
            self.view.alert("No selection provided")

    def _file_selected_evt(self, file_list: List[str]):
        """
        Adds all selected files to the GUI.

        Parameters
        ----------
        file_list : List[str]
            The list of files
        """
        if file_list is None or len(file_list) < 1:
            self.view.alert("No selection provided")
        else:
            for file in file_list:
                if self.is_supported(file):
                    self.view.file_widget.add_new_item(file)
                else:
                    self.view.alert("Unsupported file type:" + file)

    def start_annotating(self, row: Optional[int] = 0):
        """Set current item to the first item."""
        if self.view.file_widget.count() > 0:
            self.view.file_widget.setCurrentItem(self.view.file_widget.item(row))

        else:
            self.view.alert("No files to annotate")

    def stop_annotating(self):
        """Clear file widget and reset buttons."""
        self.view.file_widget.clear_all()
        self.view.reset_buttons()

    def curr_img_dict(self) -> Dict[str, str]:
        """
         Return a dictionary with the current image File Path
         and row in the list.

        Returns
        ----------
        Dict[str,str]
            dictionary of file name and row attributes.
        """
        item = self.view.file_widget.currentItem()
        info = {
            "File Path": item.file_path,
            "Row": str(self.view.file_widget.get_curr_row()),
        }
        return info

    def next_img(self):
        """
        Set the current image to the next in the list, stop incrementing
        at the last row.
        """
        if self.view.file_widget.get_curr_row() < self.view.file_widget.count() - 1:
            self.view.file_widget.setCurrentItem(self.view.file_widget.item(self.view.file_widget.get_curr_row() + 1))

    def prev_img(self):
        """Set the current image to the previous in the list, stop at first image."""
        if self.view.file_widget.get_curr_row() > 0:
            self.view.file_widget.setCurrentItem(self.view.file_widget.item(self.view.file_widget.get_curr_row() - 1))

    def get_num_files(self) -> int:
        """
        Returns
        ----------
        int
            number of files.
        """
        return self.view.file_widget.count()

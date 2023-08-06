import os.path
import datetime
import numpy as np
import pandas as pd
from PyQt6 import uic
from PyQt6.QtWidgets import \
    QMainWindow, \
    QApplication, \
    QFileDialog, \
    QMessageBox, \
    QWidget, \
    QComboBox, \
    QLabel, \
    QHBoxLayout, \
    QGridLayout
from PyQt6.QtCore import QThreadPool, QObject, QRunnable, pyqtSignal, pyqtSlot
import pyqtgraph as pg
from resilipy.scripts.dataframe_reader import TableModel


class PhaseCheckRow(QWidget):
    """
    When the files are loaded, the user can check and if necessary change the phase of each loaded data sheet.
    Each row of this is represented by a PhaseCheckRow object.
    """
    def __init__(self, information: dict):
        super(PhaseCheckRow, self).__init__()
        # assign member variables
        self.id = information["id"]
        self.file_name = information["file_name"]
        self.sheet_name = information["sheet_name"]
        self.phase = information["phase"]
        self.data = information["data"].to_numpy()
        self.cage_pos = information["cage_pos"]

        # coordinates needed for drawing the cage position in the graph
        self.x_min, self.x_max = np.amin(self.data[:, 0]), np.amax(self.data[:, 0])
        self.y_min, self.y_max = np.amin(self.data[:, 1]), np.amax(self.data[:, 1])

        self.cage_pos_l = (self.x_min + (self.x_max - self.x_min) / 5, (self.y_max + self.y_min) / 2)
        self.cage_pos_r = (self.x_max - (self.x_max - self.x_min) / 5, (self.y_max + self.y_min) / 2)
        self.cage_pos_t = ((self.x_max + self.x_min) / 2, self.y_max - (self.y_max - self.y_min) / 5)
        self.cage_pos_b = ((self.x_max + self.x_min) / 2, self.y_min + (self.y_max - self.y_min) / 5)

        # init static labels
        self.label_id = QLabel("ID: ")
        self.label_filename = QLabel("File name: ")
        self.label_sheetname = QLabel("Sheet name: ")
        self.label_cagepos = QLabel("Phase position")
        # init changing labels
        self.labelId = QLabel(self.id)
        self.labelFileName = QLabel(self.file_name)
        self.labelSheetName = QLabel(self.sheet_name)
        # init combo boxes
        self.phaseOptions = QComboBox()
        self.cageOptions = QComboBox()
        self.setup_combo_box()
        self.cageOptions.currentIndexChanged.connect(self.__draw_cage)
        # set up graph
        self.graph = pg.PlotWidget()
        self.cage = pg.ScatterPlotItem(size=8, brush=pg.mkBrush("red"))
        self.setup_graph()
        # set up layout
        self.setup_layout()

    def setup_combo_box(self):
        """
        Adds items to the two combo (phase & cage position) boxes and sets the initial option
        """
        self.phaseOptions.addItems(["habituation", "test"])
        if self.phase == "habituation":
            self.phaseOptions.setCurrentIndex(0)
        else:
            self.phaseOptions.setCurrentIndex(1)

        self.cageOptions.addItems(["left", "right", "top", "bottom"])
        # when initializing the cage pos can only be left or right
        if self.cage_pos == "left":
            self.cageOptions.setCurrentIndex(0)
        else:
            self.cageOptions.setCurrentIndex(1)

    def change_cage_pos(self, i: int):
        """
        Sets comboBox to Index i. Used when changing indices of all rows.
        """
        self.cageOptions.setCurrentIndex(i)

    def setup_graph(self):
        """
        Sets up the graph containing the positions of the mouse.
        """
        self.graph.setInteractive(False)
        self.graph.setFixedSize(200, 200)
        self.graph.setBackground("w")

        scatter = pg.ScatterPlotItem(size=5, brush=pg.mkBrush("grey"))
        scatter.setData(self.data[:, 0], self.data[:, 1])
        self.graph.addItem(scatter)

        self.__draw_cage()

    def __draw_cage(self):
        """
        Adds a red dot indicating the position of the cage (left/right/top/bottom)
        """
        self.graph.removeItem(self.cage)
        self.cage_pos = self.cageOptions.currentText()
        if self.cage_pos == "left":
            self.cage.setData([self.cage_pos_l[0]], [self.cage_pos_l[1]])
        elif self.cage_pos == "right":
            self.cage.setData([self.cage_pos_r[0]], [self.cage_pos_r[1]])
        elif self.cage_pos == "top":
            self.cage.setData([self.cage_pos_t[0]], [self.cage_pos_t[1]])
        else:
            self.cage.setData([self.cage_pos_b[0]], [self.cage_pos_b[1]])
        self.graph.addItem(self.cage)

    def setup_layout(self):
        """
        Adds all widgets to the layout in order to get the graph on the left and the information and combo boxes
        on the right in a vertical layout.
        """
        layout = QHBoxLayout()
        layout_inner = QGridLayout()
        layout_inner.addWidget(QLabel("ID: "), 0, 0)
        layout_inner.addWidget(self.labelId, 0, 1)

        layout_inner.addWidget(QLabel("File name: "), 1, 0)
        layout_inner.addWidget(self.labelFileName, 1, 1)

        layout_inner.addWidget(QLabel("Sheet name: "), 2, 0)
        layout_inner.addWidget(self.labelSheetName, 2, 1)

        layout_inner.addWidget(QLabel("Phase: "), 3, 0)
        layout_inner.addWidget(self.phaseOptions, 3, 1)

        layout_inner.addWidget(QLabel("Cage position: "), 4, 0)
        layout_inner.addWidget(self.cageOptions, 4, 1)
        layout.addWidget(self.graph)
        layout.addLayout(layout_inner)
        self.setLayout(layout)

    def get_selection(self) -> (str, str):
        return self.phaseOptions.currentText(), self.cageOptions.currentText()


class WorkerSignals(QObject):
    progress = pyqtSignal(str)
    loaded_data = pyqtSignal(list)


class Worker(QRunnable):

    def __init__(self, file_paths: [str]):
        super(Worker, self).__init__()
        self.signals = WorkerSignals()
        self.file_paths = file_paths

    def __find_user_variables(self, data: pd.DataFrame, start_index: int):
        """
        Extracts the user-defined variables from the dataset
        """
        user_var_start_ind = data.loc[data[0] == "User-defined Independent Variable"].index[0] + 1
        user_vars = data.iloc[user_var_start_ind:start_index-3, :2]
        data_id = user_vars.iloc[0, 1]
        # if the ID is not given
        if not type(data_id) == str:
            data_id = "unknown"
        return data_id, user_vars

    def __find_phase(self, data: pd.DataFrame) -> str:
        """
        Extracts the data phase from the user-defined data
        """
        if data.eq("habituation").any().any():
            phase = "habituation"
        elif data.eq("test").any().any():
            phase = "test"
        else:
            phase = "unknown"
        return phase

    @pyqtSlot()
    def run(self):
        info_list = []
        for path in self.file_paths:
            file = pd.ExcelFile(path)
            file_name = os.path.basename(path)
            # first sheet -> cage on right side; second sheet -> cage on left side
            sheet_no = 1
            for sheet in file.sheet_names:
                information = {}
                self.signals.progress.emit("Loading: file {}, sheet {}".format(file_name, sheet))

                data = file.parse(sheet_name=sheet, header=None)
                start_index = int(data[1][0])

                data_id, user_vars = self.__find_user_variables(data, start_index)
                phase = self.__find_phase(user_vars)
                raw_data = pd.DataFrame(data=data[start_index:])
                raw_data.columns = data.iloc[start_index - 2, :]
                raw_data.reset_index(drop=True, inplace=True)

                # add the ID, the phase information and the raw data to of each
                information["id"] = data_id
                information["file_name"] = file_name
                information["sheet_name"] = sheet
                information["data"] = raw_data
                information["phase"] = phase
                if (sheet_no % 2) == 1:
                    information["cage_pos"] = "left"
                else:
                    information["cage_pos"] = "right"
                sheet_no += 1

                info_list.append(information)
                self.signals.progress.emit("Done")

        self.signals.loaded_data.emit(info_list)


class Preprocessor(QMainWindow):

    file_paths: [str] = []
    loaded_data: [dict] = []
    """
    loaded data contains:   ID, file name, sheet name, phase, data,
                            center position available,
                            nose position available,
                            cage position
    """
    final_data: pd.DataFrame
    was_exported: bool = False
    phase_check_rows = [PhaseCheckRow]

    def __init__(self):
        super().__init__()
        dirname = os.path.dirname(__file__)
        ui = os.path.join(dirname, "../ui/preprocessor.ui")
        uic.loadUi(ui, self)

        self.threadpool = QThreadPool()

        self.pushButtonSelect.clicked.connect(self.select_files)
        self.pushButtonRemove.clicked.connect(self.remove_files)
        self.buttonLoadFiles.clicked.connect(self.decide_load_data)

        self.comboCagePosCentral.currentIndexChanged.connect(self.change_all_cage_pos)

        self.buttonStartTransform.clicked.connect(self.transform_data)
        self.buttonExport.clicked.connect(self.export_data)
        self.buttonClose.clicked.connect(self.close_window)

        ### Navigation buttons ###
        self.buttonNext0.clicked.connect(self.next_page_0)
        self.buttonBack1.clicked.connect(self.back_page_1)
        self.buttonNext1.clicked.connect(self.next_page_1)
        self.buttonBack2.clicked.connect(self.back_page_2)

        self.set_up_style()

    def set_up_style(self):
        """
        Reads and sets up the stylesheet.
        """
        dirname = os.path.dirname(__file__)
        path = os.path.join(dirname, "../ui/stylesheet.txt")
        with open(path) as file:
            stylesheet = file.read()
            self.setStyleSheet(stylesheet)

    def next_page_0(self):
        """
        Switches from page 0 (starting page) to page 1
        """
        self.stackedWidget.setCurrentIndex(1)

    def back_page_1(self):
        """
        Switches from page 1 to page 0
        """
        self.stackedWidget.setCurrentIndex(0)

    def next_page_1(self):
        """
        Switches from page 1 to page 2
        """
        self.update_phases()
        self.stackedWidget.setCurrentIndex(2)

    def back_page_2(self):
        """
        Switches from page 2 to page 1
        """
        self.stackedWidget.setCurrentIndex(1)

    def __remove_duplicates(self, lst: [str]) -> [str]:
        """
        Removes duplicate strings from a list of strings
        """
        return list(dict.fromkeys(lst))

    def __update_path_list(self):
        """
        Clears and refills the list widget. Method is called when select_files or remove_files is called
        """
        self.listFilePaths.clear()
        self.listFilePaths.addItems(self.file_paths)

    def select_files(self):
        """
        Allows the user to select xlsx files and displays the selected files in the list widget
        """
        dir_dialog = QFileDialog(self)
        file_names = dir_dialog.getOpenFileNames(caption="Select all files of the batch", filter="Excel (*.xlsx)")
        self.file_paths += file_names[0]

        self.file_paths = self.__remove_duplicates(self.file_paths)
        if len(self.file_paths) > 0:
            self.file_paths.sort()
            self.__update_path_list()
            self.pushButtonRemove.setEnabled(True)
            self.buttonLoadFiles.setEnabled(True)

    def remove_files(self):
        """
        Removes selected items from the list widget
        """
        to_remove = self.listFilePaths.selectedItems()
        if len(to_remove) > 0:
            # turns the list of QListWidgetItem into a list of strings
            to_remove = list(map(lambda x: x.text(), to_remove))
            # removes the strings that are present in to_remove from the file_paths list
            self.file_paths = [path for path in self.file_paths if path not in to_remove]
            self.__update_path_list()

            if len(self.file_paths) == 0:
                self.pushButtonRemove.setEnabled(False)
                self.buttonLoadFiles.setEnabled(False)

    def __assign_phase_when_unknown(self):
        """
        Assigns a phase to a dataset in case it was not given. For each animal, two sheets must be given.
        One from habituation and one from test phase. It is expected that the sheet that is loaded first
        corresponds to the habituation and the second to the test phase. The phases are assigned accordingly.
        """
        ids = []
        for item in self.loaded_data:
            if item["phase"] == "unknown":
                if item["id"] in ids:
                    item["phase"] = "test"
                else:
                    item["phase"] = "habituation"
                    ids.append(item["id"])

    def __load_progress(self, progress: str):
        """
        Updates the text in the text browser when loading the files
        """
        self.textLoadedProgress.append(progress)

    def __set_loaded_data(self, loaded_data):
        """
        Assigns the returned list to the member variable
        """
        self.loaded_data = loaded_data
        self.__assign_phase_when_unknown()

        self.preprocess_information()

        self.display_loaded_data()

        # enable buttons again
        self.buttonNext0.setEnabled(True)
        self.pushButtonSelect.setEnabled(True)
        self.pushButtonRemove.setEnabled(True)
        self.buttonLoadFiles.setEnabled(True)

    def decide_load_data(self):
        """
        If data was loaded before, opens a Messagebox to let the user decide whether the load process should be done
        again.
        """
        if len(self.loaded_data) > 0:
            info_box = QMessageBox.question(self, "Continue?", "Data was already loaded. Do you want to load the files above?",
                                            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                            defaultButton=QMessageBox.StandardButton.No)
            if info_box == QMessageBox.StandardButton.No:
                return
        self.load_data()

    def load_data(self):
        """
        Starts another threat that loads the files that are given
        """
        if len(self.file_paths) > 0:
            # clear the text browser containing the progress (in case something has been loaded before)
            self.textLoadedProgress.clear()
            # disable buttons
            self.buttonNext0.setEnabled(False)
            self.pushButtonSelect.setEnabled(False)
            self.pushButtonRemove.setEnabled(False)
            self.buttonLoadFiles.setEnabled(False)

            # another thread is used for loading the files, as it does not freeze the window this way
            worker = Worker(self.file_paths)
            worker.signals.progress.connect(self.__load_progress)
            # get the loaded data
            worker.signals.loaded_data.connect(self.__set_loaded_data)

            self.threadpool.start(worker)

    def preprocess_information(self):
        """
        processes the loaded data in a way that only the necessary columns remain in numerical form without null
        values. Two possibilities:
        1:  Only the center positions are available => Only compute the percentiles and nearCage values based on the
            center positions
        2:  Center and nose positions are available => Use nose positions for percentiles and nearCage and implement
            nearLook measure as well

        Adds a sixth element to each loaded dataset: dict containing information about whether the nose and center
        tracking data is available
        """
        for i in range(len(self.loaded_data)):
            data_info = {}
            data = self.loaded_data[i]["data"]
            cols = data.columns

            # check whether the center and/or the nose positions are available
            nose_available = False
            center_available = False
            if "X nose" in cols and "Y nose" in cols:
                nose_available = True
            if "X center" in cols and "Y center" in cols:
                center_available = True

            if nose_available and center_available:
                data = data.loc[:, ["X nose", "Y nose", "X center", "Y center"]]
            elif nose_available and not center_available:
                data = data.loc[:, ["X nose", "Y nose"]]
            elif not nose_available and center_available:
                data = data.loc[:, ["X center", "Y center"]]
            else:
                raise Exception("Neither center, nor nose positions were found in the dataset.\n"
                                "Following columns names need to be found in the dataset:"
                                " 'X center'+'Y center' and/or 'X nose'+'Y nose'.\n"
                                " Columns found in dataset: {}".format(cols))
            self.loaded_data[i]["nose"] = nose_available
            self.loaded_data[i]["center"] = center_available

            data = data.apply(pd.to_numeric, errors="coerce")
            data.dropna(inplace=True)

            self.loaded_data[i]["data"] = data

    def __reset_rows(self):
        """
        Clears the form layout
        """
        for i in reversed(range(self.formLayoutImported.count())):
            self.formLayoutImported.itemAt(i).widget().setParent(None)

    def display_loaded_data(self):
        """
        Adds a row to the FormLayout for each of the loaded files. The user can then check if the phase is
        assigned correctly.
        """
        self.__reset_rows()
        self.phase_check_rows = []
        for loaded_file in self.loaded_data:
            row = PhaseCheckRow(loaded_file)
            self.phase_check_rows.append(row)
            self.formLayoutImported.addRow(row)

    def change_all_cage_pos(self):
        """
        Sets the cage position of all rows to the value selected in the combobox.
        """
        pos = self.comboCagePosCentral.currentText()
        if pos == "left":
            pos_index = 0
        elif pos == "right":
            pos_index = 1
        elif pos == "top":
            pos_index = 2
        elif pos == "bottom":
            pos_index = 3
        else:
            return
        self.__update_all(pos_index)

    def __update_all(self, pos: int):
        """
        Changes the selection of the cage position for all rows.
        """
        for i in range(len(self.phase_check_rows)):
            self.phase_check_rows[i].change_cage_pos(pos)

    def update_phases(self):
        """
        After the user checks whether all phases are assigned correctly, the selection is updated again
        """
        for i in range(len(self.loaded_data)):
            self.loaded_data[i]["phase"], self.loaded_data[i]["cage_pos"] = self.phase_check_rows[i].get_selection()

    def transform_data(self):
        """
        Finally transforms the raw data into the alternative form
        """
        hab = pd.DataFrame(columns=["id", "10%_habituation", "25%_habituation", "50%_habituation", "75%_habituation", "nearCage_habituation", "nearLook_habituation"])
        test = pd.DataFrame(columns=["id", "10%_test", "25%_test", "50%_test", "75%_test", "nearCage_test", "nearLook_test"])
        for info in self.loaded_data:
            measures = [info["id"]]
            measures += self.transform_dataset(info)
            if info["phase"] == "habituation":
                hab.loc[len(hab.index)] = measures
            else:
                test.loc[len(test.index)] = measures

        self.final_data = hab.set_index("id").join(test.set_index("id"), how="outer")

        self.display_final_data()

    def transform_dataset(self, info: dict) -> list:
        """
        Extracts the 10th, 25th, 50th and 75th percentiles of the distribution of the normalized distance to the cage
        from the data, as well as the mean value of the nearCage and nearLook measure (nearLook only if the nose
        position is available)
        """
        center_av = info["center"]
        nose_av = info["nose"]

        data = info["data"]

        x_min, x_max, y_min, y_max = self.__get_min_max(data, center_av, nose_av)
        cage = self.__get_cage_coord(info["cage_pos"], x_min, x_max, y_min, y_max)
        max_dist = np.sqrt((x_min - x_max) ** 2 + (y_max - y_min) ** 2)

        if center_av and nose_av:
            data["dist_cage_norm"] = np.sqrt((data["X nose"] - cage[0]) ** 2 + (data["Y nose"] - cage[1]) ** 2) / max_dist
            data["near_cage"] = data["dist_cage_norm"].apply(lambda x: 1 if x <= 0.2 else 0)
            data["angle"] = np.rad2deg(np.arctan((data["X nose"] - data["X center"]) / (data["Y nose"] - data["Y center"]))) + 180
            data["cage_angle"] = np.rad2deg(np.arctan((data["X nose"] - cage[0]) / (data["Y nose"] - cage[1]))) + 180
            data["near_look"] = data.apply(lambda x: 0 if abs(x["cage_angle"] - x["angle"]) > 60 else x["near_cage"], axis=1)
            quantiles = [data["dist_cage_norm"].quantile(0.1),
                         data["dist_cage_norm"].quantile(0.25),
                         data["dist_cage_norm"].quantile(0.5),
                         data["dist_cage_norm"].quantile(0.75),
                         np.mean(data["near_cage"]),
                         np.mean(data["near_look"])]

        elif center_av:
            data["dist_cage_norm"] = np.sqrt((data["X center"] - cage[0]) ** 2 + (data["Y center"] - cage[1]) ** 2) / max_dist
            data["near_cage"] = data["dist_cage_norm"].apply(lambda x: 1 if x <= 0.2 else 0)
            quantiles = [data["dist_cage_norm"].quantile(0.1),
                         data["dist_cage_norm"].quantile(0.25),
                         data["dist_cage_norm"].quantile(0.5),
                         data["dist_cage_norm"].quantile(0.75),
                         np.mean(data["near_cage"]),
                         np.NaN]
        elif nose_av:
            data["dist_cage_norm"] = np.sqrt((data["X nose"] - cage[0]) ** 2 + (data["Y nose"] - cage[1]) ** 2) / max_dist
            data["near_cage"] = data["dist_cage_norm"].apply(lambda x: 1 if x <= 0.2 else 0)
            quantiles = [data["dist_cage_norm"].quantile(0.1),
                         data["dist_cage_norm"].quantile(0.25),
                         data["dist_cage_norm"].quantile(0.5),
                         data["dist_cage_norm"].quantile(0.75),
                         np.mean(data["near_cage"]),
                         np.NaN]
        else:
            raise Exception("ID: {}, phase: {}\nNeither center, nor Nose coordinates were found.".format(info["id"],
                                                                                                         info["phase"]))
        return quantiles

    def __get_min_max(self, data: pd.DataFrame, center_av: bool, nose_av: bool) -> (float, float, float, float):
        """
        Returns the minimum and maximum X and Y value found in a given dataset
        """
        if center_av and nose_av:
            x_min, x_max = data[["X center", "X nose"]].min().min(), data[["X center", "X nose"]].max().max()
            y_min, y_max = data[["Y center", "Y nose"]].min().min(), data[["Y center", "Y nose"]].max().max()
        elif center_av:
            x_min, x_max = np.min(data["X center"]), np.max(data["X center"])
            y_min, y_max = np.min(data["Y center"]), np.max(data["Y center"])
        elif nose_av:
            x_min, x_max = np.min(data["X nose"]), np.max(data["X nose"])
            y_min, y_max = np.min(data["Y nose"]), np.max(data["Y nose"])
        else:
            x_min, x_max, y_min, y_max = np.NaN, np.NaN, np.NaN, np.NaN

        return x_min, x_max, y_min, y_max

    def __get_cage_coord(self, cage_pos: str, x_min: float, x_max: float, y_min: float, y_max: float) -> (float, float):
        """
        Returns the approximate coordinates of the cage
        """
        if cage_pos == "left":
            cage = (x_min + (x_max - x_min) / 5, (y_max + y_min) / 2)
        elif cage_pos == "right":
            cage = (x_max - (x_max - x_min) / 5, (y_max + y_min) / 2)
        elif cage_pos == "top":
            cage = ((x_max + x_min) / 2, y_max - (y_max - y_min) / 5)
        else:
            cage = ((x_max + x_min) / 2, y_min + (y_max - y_min) / 5)
        return cage

    def display_final_data(self):
        """
        Displays the transformed data in the TableView widget.
        """
        self.tableViewFinal.setModel(TableModel(self.final_data.round(4)))
        self.buttonExport.setEnabled(True)

    def export_data(self):
        """
        Allows the user export the transformed data as csv.
        """
        now = datetime.datetime.now()
        path_save, _ = QFileDialog.getSaveFileName(self, "Save file", now.strftime("/home/export_%y_%m_%d_%H_%M_%S"), "CSV (*.csv *.CSV)")
        if path_save:
            self.final_data.to_csv(path_save)
            self.was_exported = True

    def close_window(self):
        """
        Opens a warning if the data has not been exported yet.
        """
        if not self.was_exported:
            info_box = QMessageBox.question(self, "Close window?",
                                            "You did not export any data. Are you sure that you want to close the window?",
                                            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                            defaultButton=QMessageBox.StandardButton.No)
            if info_box == QMessageBox.StandardButton.No:
                return
        QApplication.instance().quit()


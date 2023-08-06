import os
import pickle
import pandas as pd
import numpy as np

from resilipy.scripts.dataframe_reader import TableModel

from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis

from PyQt6 import uic
from PyQt6.QtWidgets import \
    QMainWindow, \
    QApplication, \
    QFileDialog, \
    QMessageBox, \
    QCheckBox
from PyQt6.QtCore import Qt


class Builder(QMainWindow):
    name: str
    description: str
    model = None
    __dataset_type: str
    training_data_raw: pd.DataFrame = None

    __target_col: str
    __important_cols_widgets = []
    important_cols = [str]

    training_target: pd.Series
    training_features: pd.DataFrame
    training_features_ohe: pd.DataFrame

    def __init__(self):
        super().__init__()
        dirname = os.path.dirname(__file__)
        ui = os.path.join(dirname, "../ui/builder.ui")
        uic.loadUi(ui, self)

        self.buttonLoadModel.pressed.connect(self.load_model)
        self.buttonDeleteModel.pressed.connect(self.delete_model)

        self.buttonLoadData.pressed.connect(self.load_dataset)
        self.buttonDeleteData.pressed.connect(self.delete_dataset)

        self.buttonTargetConfirm.pressed.connect(self.setup_imp_col_selection)
        self.buttonTargetUndo.pressed.connect(self.undo_imp_col_selection)

        self.buttonFinish.pressed.connect(self.finish_model)

        # Navigation
        self.buttonNext0.pressed.connect(self.next0)
        self.buttonBack1.pressed.connect(self.back1)
        self.buttonNext1.pressed.connect(self.next1)
        self.buttonBack2.pressed.connect(self.back2)
        self.buttonNext2.pressed.connect(self.next2)
        self.buttonBack3.pressed.connect(self.back3)
        self.buttonNext3.pressed.connect(self.next3)
        self.buttonBack4.pressed.connect(self.back4)

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

    def next0(self):
        """
        Switches to page 2 (index from 0 to 1) if both the name and description were given.
        """
        name_given = self.get_name()
        descr_given = self.get_description()

        if name_given and descr_given:
            self.stackedWidget.setCurrentIndex(1)
        elif not name_given and descr_given:
            QMessageBox.critical(self, "Missing information",
                                 "No name was given. Please input the name into the line edit.")
        elif name_given and not descr_given:
            QMessageBox.critical(self, "Missing information",
                                 "No description was given. Please input the description of the model into the "
                                 "text edit.")
        else:
            QMessageBox.critical(self, "Missing information",
                                 "Neither name, nor description were given. Please input both into the corresponding "
                                 "input fields.")

    def get_name(self) -> bool:
        """
        Assigns the user input of the name lineEdit to the member variable. If an input is given, returns True.
        """
        name_ = self.lineEditName.text()
        if len(name_) > 0:
            self.name = name_
            return True
        else:
            return False

    def get_description(self) -> bool:
        """
        Assigns the user input of the description textEdit to the member variable. If an input is given, returns True.
        """
        description = self.textEditDescription.toPlainText()
        if len(description) > 0:
            self.description = description
            return True
        else:
            return False

    def back1(self):
        self.stackedWidget.setCurrentIndex(0)

    def load_model(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select pickled model", "/home")
        try:
            with open(path, 'rb') as file:
                loaded = pickle.load(file)

            if self.is_classifier(loaded):
                self.model = loaded
                self.textBrowserModel.clear()
                self.textBrowserModel.setPlainText(self.model.__repr__())
            else:
                QMessageBox.critical(self, "File not compatible",
                                     "Loaded file is not a compatible classifier. The following sklearn classifiers are "
                                     "supported:")
        except:
            QMessageBox.critical(self, "File not compatible",
                                 "Could not read the selected file. Make sure that the file contains a pickles sklearn "
                                 "classifier.")

    def delete_model(self):
        """
        Deletes the currently loaded model and clears the text browser.
        """
        self.model = None
        self.textBrowserModel.clear()

    def is_classifier(self, model) -> bool:
        """
        Checks whether the imported file is one of the classifiers from sklearn.
        Checks if the loaded data type is one of the following:
        - LogisticRegression
        - MLPClassifier
        - KNeighborsClassifier
        - SVC
        - GaussianProcessClassifier
        - DecisionTreeClassifier
        - RandomForestClassifier
        - AdaBoostClassifier
        - GaussianNB
        - QuadraticDiscriminantAnalysis
        - XGBClassifier
        """
        classifiers = [LogisticRegression,
                       XGBClassifier,
                       MLPClassifier,
                       KNeighborsClassifier,
                       SVC,
                       GaussianProcessClassifier,
                       DecisionTreeClassifier,
                       RandomForestClassifier,
                       AdaBoostClassifier,
                       GaussianNB,
                       QuadraticDiscriminantAnalysis]
        for classifier in classifiers:
            if type(model) == classifier:
                return True
        return False

    def next1(self):
        """
        Checks if a model was loaded and if that is the case, switches to the next page.
        """
        if self.model is None:
            QMessageBox.critical(self, "No model loaded.",
                                 "No model was loaded. Please select a pickled sklearn classifier.")
            return
        self.stackedWidget.setCurrentIndex(2)

    def back2(self):
        self.stackedWidget.setCurrentIndex(1)

    def load_dataset(self):
        """
        Loads the training dataset.
        """
        index_col = self.get_index_col()
        sep = self.get_separator()
        if not index_col:
            button = QMessageBox.question(self, "No index column",
                                          "No name for the index column was given. "
                                          "If the dataset has an index column please specify it in the field above "
                                          "to avoid errors. If the dataset has no index column, just continue. \n\n"
                                          "Do you want to continue?")
            if button == QMessageBox.StandardButton.No:
                return

        path_import, _ = QFileDialog.getOpenFileName(self, "Open File", "/home", "CSV (*.csv *.CSV)")
        if path_import:
            imported_data = pd.read_csv(path_import, sep=sep)
            col_names_import = imported_data.columns.to_list()

            if imported_data.shape[1] == 1:
                QMessageBox.critical(self, "Wrong separator!",
                                     "It appears that a wrong separator was selected. Please select the correct one.")
                return

            if index_col and (index_col not in col_names_import):
                QMessageBox.critical(self, "Index column not found!",
                                     "The given column name '{}' was not found in the imported dataset.".format(index_col))
                return

            self.training_data_raw = imported_data
            if index_col:
                self.training_data_raw = self.training_data_raw.set_index(index_col)

            self.tableViewRaw.setModel(TableModel(np.round(self.training_data_raw, 3)))

    def get_index_col(self) -> str:
        """
        returns the index column given by the user.
        """
        return self.lineEditIndex.text()

    def get_separator(self) -> str:
        """
        Returns the separator selected by the user.
        """
        if self.radioComma.isChecked():
            sep = ","
        elif self.radioSemicolon.isChecked():
            sep = ";"
        elif self.radioTab.isChecked():
            sep = "\t"
        elif self.radioSpace.isChecked():
            sep = "\s+"
        return sep

    def delete_dataset(self):
        self.training_data_raw = None
        self.tableViewRaw.setModel(None)

    def next2(self):
        """
        Checks if a training dataset was loaded and if that is the case, switches to the next page.
        """
        if self.training_data_raw is None:
            QMessageBox.critical(self, "No dataset loaded.",
                                 "No training dataset was loaded. Please select a CSV file.")
            return
        self.get_data_type()
        self.fill_combobox_target()
        self.stackedWidget.setCurrentIndex(3)

    def get_data_type(self):
        """
        Gets the selection from the radio button that determines if the dataset is already in OHE form.
        """
        if self.radioTypeRaw.isChecked():
            self.__dataset_type = "raw"
        elif self.radioTypeOhe.isChecked():
            self.__dataset_type = "ohe"

    def back3(self):
        self.stackedWidget.setCurrentIndex(2)

    def fill_combobox_target(self):
        """
        Adds all columns of the dataset to the combobox. The one that is selected is chosen as the target column.
        The currently selected column is not shown in the check boxes below
        """
        self.comboBoxTarget.addItems(self.training_data_raw.columns)

    def setup_imp_col_selection(self):
        """
        When the target column was confirmed, the Checkboxes are loaded.
        """
        self.__target_col = self.comboBoxTarget.currentText()

        # Enable/disable the widgets of the target column assignment
        self.comboBoxTarget.setEnabled(False)
        self.buttonTargetConfirm.setEnabled(False)
        self.buttonTargetUndo.setEnabled(True)
        # get the target and features from the raw data
        self.process_raw_data()
        # set up the checkboxes for each column
        self.setup_check_boxes()

    def process_raw_data(self):
        """
        Extracts features and target from the raw dataset
        """
        self.training_target = self.training_data_raw[self.__target_col]
        self.training_features = self.training_data_raw.drop(self.__target_col, axis=1)
        if self.__dataset_type == "raw":
            self.training_features_ohe = pd.get_dummies(self.training_features)
        # if the data is already in one-hot encoded form, the two variables are the same.
        elif self.__dataset_type == "ohe":
            self.training_features_ohe = self.training_features

    def setup_check_boxes(self):
        """
        Sets up a checkbox for each column found in the dataset. The user can select which ones to keep by selecting
        these.
        """
        self.__important_cols_widgets = []

        for col in self.training_features_ohe.columns.to_list():
            checkbox = QCheckBox(str(col))
            checkbox.toggle()
            self.__important_cols_widgets.append(checkbox)
            self.layoutImpCols.addWidget(checkbox)

    def undo_imp_col_selection(self):
        """
        Deletes the check boxes in order to allow the user to select another target column.
        """
        self.clear_layout()
        self.comboBoxTarget.setEnabled(True)
        self.buttonTargetConfirm.setEnabled(True)
        self.buttonTargetUndo.setEnabled(False)

    def clear_layout(self):
        """
        Removes all checkboxes from the layout.
        Source: https://stackoverflow.com/questions/4528347/clear-all-widgets-in-a-layout-in-pyqt
        """
        for i in reversed(range(self.layoutImpCols.count())):
            self.layoutImpCols.itemAt(i).widget().setParent(None)

    def next3(self):
        """
        Switches to page 3 after the user confirms the selection.
        """
        self.get_selection()
        button = QMessageBox.question(self, "Confirm selection",
                                      "The following columns were selected:\n"
                                      "Target column: {}\nImportant columns: {}\nAre these selections correct?"
                                      .format(self.__target_col, self.important_cols))
        if button == QMessageBox.StandardButton.No:
            return
        self.set_up_summary()
        self.stackedWidget.setCurrentIndex(4)

    def get_selection(self):
        """
        Stores all checked columns in a list
        """
        self.important_cols = []
        for checkbox in self.__important_cols_widgets:
            if checkbox.checkState() == Qt.CheckState.Checked:
                self.important_cols.append(checkbox.text())
        self.training_features_ohe = self.training_features_ohe[self.important_cols]

    def set_up_summary(self):
        """
        Summarises the information on the last page.
        """
        self.textBrowserSumName.setText(self.name)
        self.textBrowserSumDescr.setText(self.description)
        self.textBrowserSumClassifier.setText(self.model.__repr__())
        self.tableSumFeatures.setModel(TableModel(np.round(self.training_features_ohe, 2)))

    def finish_model(self):
        model = {}
        model["name"] = self.name
        model["description"] = self.description
        model["classifier"] = self.model
        model["training_data_raw"] = self.training_data_raw
        model["training_features"] = self.training_features
        model["training_target"] = self.training_target
        model["training_data_ohe"] = self.training_features_ohe
        model["important_cols"] = self.important_cols

        # https://stackoverflow.com/questions/9856683/using-pythons-os-path-how-do-i-go-up-one-directory
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models'))
        with open("{}/{}".format(path, self.name), "wb") as file:
            pickle.dump(model, file)

        QMessageBox.information(self, "Finished", "The model was successfully saved in the 'models' folder.")
        QApplication.instance().quit()

    def back4(self):
        """
        Switches to the previous page.
        """
        self.textBrowserSumName.clear()
        self.textBrowserSumDescr.clear()
        self.textBrowserSumClassifier.clear()
        self.tableSumFeatures.setModel(None)

        self.stackedWidget.setCurrentIndex(3)


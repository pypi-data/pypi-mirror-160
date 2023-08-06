import os
import pickle
import datetime
import sys

import pandas as pd
import numpy as np
import Levenshtein

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
from sklearn.model_selection import train_test_split

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
    QRadioButton
from PyQt6.QtCore import QThreadPool, QObject, QRunnable, pyqtSignal, pyqtSlot


class ColumnAssignment(QWidget):
    """
    Represents one column in the form layout during the column assignment.
    Consists of a label showing the name of a column
    from the training dataset (__column_name_training) and
    a combo box next to the label to assign a column
    from the imported dataset (given through __options).
    """
    __column_name_training: str
    __options: [str]
    __current_selection: str

    def __init__(self, text, options):
        super().__init__()
        self.__column_name_training = text
        self.__options = options
        self.find_in_options()
        self.__current_selection = self.__options[0]

        self.label_col_name = QLabel(self.__column_name_training)
        self.combo_box = QComboBox()
        self.combo_box.addItems(self.__options)

        layout = QHBoxLayout()
        layout.addWidget(self.label_col_name)
        layout.addWidget(self.combo_box)
        self.setLayout(layout)

        self.combo_box.currentIndexChanged.connect(self.update_selection)

    def update_selection(self):
        self.__current_selection = self.combo_box.currentText()

    def get_information(self):
        """
        Transfer the selection pairs to the Labeler object.

        :return:
        Pair consisting of the training column name
        and the selected column from the imported data.
        """
        return self.__column_name_training, self.__current_selection

    def find_in_options(self):
        """
        Used the Levenshtein distance to get the column name
        from the imported dataset that is closest
        to the current name of the column from the training dataset.
        The closest is put at the first position of the options list,
        so it is selected as the default.
        """
        closest_ind = 0
        min_distance = Levenshtein.distance(self.__column_name_training, self.__options[0])

        for i in range(1, len(self.__options)):
            distance = Levenshtein.distance(self.__column_name_training, self.__options[i])
            if distance <= min_distance:
                min_distance = distance
                closest_ind = i

        if closest_ind != 0:
            col_name = self.__options[closest_ind]

            self.__options.pop(closest_ind)
            self.__options.insert(0, col_name)


class WorkerSignals(QObject):
    progress = pyqtSignal(str)
    iteration = pyqtSignal(int)
    predictions = pyqtSignal(pd.DataFrame)


class Worker(QRunnable):
    __training_features: pd.DataFrame
    __training_targets: pd.Series
    __classifier = 0
    __import_data: pd.DataFrame
    __predicted: [int]
    __predictions: pd.DataFrame

    def __init__(self, train_features, train_targets, classifier, import_data):
        super(Worker, self).__init__()
        self.signals = WorkerSignals()
        self.__import_data = import_data
        self.__predictions = pd.DataFrame(index=self.__import_data.index)

        self.__training_features = train_features
        self.__training_targets = train_targets
        self.__classifier = classifier

    @pyqtSlot()
    def run(self):
        for i in range(100):
            self.signals.progress.emit("[Iteration %d] Subsetting training data" % (i + 1))
            train_features, test_features, train_labels, test_labels = \
                train_test_split(self.__training_features, self.__training_targets)
            self.signals.progress.emit("DONE")

            self.signals.progress.emit("[Iteration %d] Fitting training data to model" % (i + 1))
            self.__classifier.fit(train_features, train_labels, eval_metric="error")
            self.signals.progress.emit("DONE")

            self.signals.progress.emit("[Iteration %d] Predicting labels" % (i + 1))
            self.__predicted = self.__classifier.predict(self.__import_data)
            self.signals.progress.emit("DONE")

            self.signals.iteration.emit(int(i))
            self.__predictions[i] = self.__predicted

        self.signals.predictions.emit(self.__predictions)


class Labeler(QMainWindow):

    __models: [dict]

    __active_model: dict
    __active_classifier = 0
    __active_dataset: pd.DataFrame
    __training_features: pd.DataFrame
    __training_features_one_hot: pd.DataFrame
    __training_target: pd.Series

    __imported_data: pd.DataFrame
    __data_imported: bool = False

    __col_names_train: [str]
    __col_names_import: [str]
    __col_selection: [ColumnAssignment] = []
    __column_assignment: [tuple]
    __selection_confirmed: bool = False

    __import_categorical_cols: [str]
    __training_categorical_cols: [str]
    __imported_data_adjusted: pd.DataFrame
    __imported_one_hot: pd.DataFrame

    __labelling_summary: pd.DataFrame
    __is_finished: bool = False
    __was_exported: bool = False

    def __init__(self):
        super().__init__()
        dirname = os.path.dirname(__file__)
        ui = os.path.join(dirname, "../ui/labeler.ui")
        uic.loadUi(ui, self)

        self.threadpool = QThreadPool()

        self.stackedWidget.setCurrentIndex(0)

        # model selection
        self.setup_models()

        # Page control
        self.pushButtonCancel.pressed.connect(QApplication.instance().quit)
        self.pushButtonNext.pressed.connect(self.next_page)
        self.pushButtonBack.pressed.connect(self.previous_page)

        # Import dataset
        self.pushButtonImport.pressed.connect(self.import_dataset)
        self.pushButtonConfirmSel.pressed.connect(self.get_selections)

        # Transform dataset to one hot encoded form
        self.pushButtonTransformData.pressed.connect(self.prepare_dataset_for_label)
        self.tableOheTrain.setModel(TableModel(np.round(self.__training_features_one_hot.head(), 2)))

        # Start labelling
        self.pushStartLabel.pressed.connect(self.start_labelling)

        # save results
        self.pushButtonSave.pressed.connect(self.save_results)

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

    def setup_models(self):
        """
        Add one radio button for each model file that is placed in the "models" folder
        """
        # get all .model files that are given in the Models folder
        dirname = os.path.dirname(__file__)
        path = os.path.join(dirname, "../models")

        #path = os.path.relpath("./resilipy/models")
        file_names = os.listdir(path)

        if len(file_names) > 0:
            first = True
            for file in file_names:
                with open(path+"/"+file, "rb") as file_opened:
                    model = pickle.load(file_opened)

                radiobutton = QRadioButton(model["name"])
                radiobutton.model = model

                if first:
                    first = False
                    radiobutton.toggle()
                    self.update_model(model)

                radiobutton.toggled.connect(self.__model_switched)
                self.radioLayout.addWidget(radiobutton)
        else:
            QMessageBox.critical(self, "Files not found",
                                 "No .model files were found in the 'models' folder.")

    def __model_switched(self):
        selected = self.sender()
        if selected.isChecked():
            self.update_model(selected.model)

    def update_model(self, model: dict):
        """
        Sets the active model to the one selected via the radio buttons.
        Updates the member variables as well as the text browser and the table view to show a description
        and the training dataset on the model selection page.
        """
        try:
            self.__active_model = model
            self.__active_classifier = model["classifier"]
            self.__active_dataset = model["training_data_raw"]
            self.__training_target = model["training_target"]
            self.__training_features = model["training_features"]
            self.__training_features_one_hot = model["training_data_ohe"]

            self.textModelDescription.setText(model["description"])
            self.tableTrainingData.setModel(TableModel(np.round(self.__active_dataset, 2)))
            self.textClassifier.setText(self.__active_classifier.__repr__())

            # clear and update the table Widgets on the third page
            self.tableOheTrain.setModel(TableModel(np.round(self.__training_features_one_hot.head(), 2)))
            self.tableOheImport.setModel(None)

        except Exception as x:
            QMessageBox.critical(self, "Model not updated",
                                 "Model '{}' could not be loaded.\nError: {}".format(model["name"], x))

    def next_page(self):
        """
        Switches to the next page when the 'Next' button is pressed
        """
        current_index = self.stackedWidget.currentIndex()
        if current_index == 0:
            # if a dataset has been imported, update the column assignment to match the new training dataset
            # case the model was changed
            if self.__data_imported:
                self.reset_column_assignment()
                self.setup_column_assignment()

            self.pushButtonBack.setEnabled(True)
            # if the column assignment has not been confirmed
            if not self.__selection_confirmed:
                self.pushButtonNext.setEnabled(False)

        elif current_index == 1:
            self.pushButtonNext.setEnabled(False)

        elif current_index == 2:
            if not self.__is_finished:
                self.pushButtonNext.setEnabled(False)
            self.pushButtonNext.setText("Finish")

        elif current_index == 3:
            self.close_application()

        self.stackedWidget.setCurrentIndex(current_index + 1)

    def previous_page(self):
        """
        Switches to the previous page when the 'Go back' button is pressed
        """
        current_index = self.stackedWidget.currentIndex()

        if current_index == 1:
            self.stackedWidget.setCurrentIndex(current_index - 1)
            self.pushButtonBack.setEnabled(False)
            self.pushButtonNext.setEnabled(True)
        elif current_index == 3:
            self.pushButtonNext.setText("Next >")

        if current_index != 0:
            self.stackedWidget.setCurrentIndex(current_index - 1)

    def import_dataset(self):
        """
        Imports a given dataset from a csv file.
        The separator is chosen through radioButtons
        """
        separator = ","
        if self.radioButtonComma.isChecked():
            separator = ","
        elif self.radioButtonSemicolon.isChecked():
            separator = ";"
        elif self.radioButtonTab.isChecked():
            separator = "\t"
        elif self.radioButtonSpace.isChecked():
            separator = "\s+"

        imported_index_col = self.lineEditIndexCol.text()
        if not imported_index_col:
            button = QMessageBox.question(self, "No index column",
                                          "No name for the index column was given. "
                                          "If the dataset has an index column please specify it in the field above "
                                          "to avoid errors. If the dataset has no index column, just continue. \n\n"
                                          "Do you want to continue?")
            if button == QMessageBox.StandardButton.No:
                return

        path_import, _ = QFileDialog.getOpenFileName(self, "Open File", "/home", "CSV (*.csv *.CSV)")

        if path_import:
            temp_imported_data = pd.read_csv(path_import, sep=separator)
            temp_col_names_import = temp_imported_data.columns.to_list()

            # set index column if a column name is given and if it is found in the column names of the imported data:
            if imported_index_col and (imported_index_col in temp_col_names_import):
                index_col = self.lineEditIndexCol.text()
                temp_imported_data = temp_imported_data.set_index(index_col)
                temp_col_names_import.remove(index_col)

                if self.check_import(temp_imported_data):
                    self.finish_import(temp_imported_data, temp_col_names_import)
            # index col given but not found in dataset
            elif imported_index_col and not (imported_index_col in temp_col_names_import):
                QMessageBox.critical(self, "Index column not found!",
                                     "The given column name '%s' was not found in the imported dataset."
                                     % imported_index_col)
            # no index col given
            elif self.check_import(temp_imported_data):
                self.finish_import(temp_imported_data, temp_col_names_import)

    def check_import(self, imported_data):
        """
        Checks the shape of a given dataset. Depending on the shape, the dataset is OK and true is returned
        (exactly the shape of the training dataset or more columns). Otherwise false is returned (fewer columns
        than the training dataset).
        """
        if imported_data.shape[1] == 1:
            QMessageBox.critical(self, "Wrong separator!",
                                 "It appears that a wrong separator was selected. Please select the correct one.")
            return False
        elif imported_data.shape[1] > self.__training_features.shape[1]:
            QMessageBox.warning(self, "Warning",
                                "Imported dataset has more columns than the training data."
                                "\nAdditional columns will not be regarded.")
            return True
        elif imported_data.shape[1] < self.__training_features.shape[1]:
            QMessageBox.critical(self, "Error",
                                 "Dataset contains fewer columns than the training data.")
            return False
        else:
            return True

    def finish_import(self, temp_imported_data: pd.DataFrame, temp_col_names_import: list):
        """
        Finishes the import of the data and assigns the dataset and the column names to the attributes,
        if the index column is given correctly and the shape of the dataset does not suggest a wrong separator.
        :param temp_imported_data: Dataset chosen during the import
        :param temp_col_names_import: Column names of the dataset
        """
        self.__imported_data = temp_imported_data
        self.__col_names_import = temp_col_names_import

        # display the imported dataset in the tableView and initializes the column assignment
        self.tableImported.setModel(TableModel(np.round(self.__imported_data.head(5), 2)))

        self.setup_column_assignment()
        self.__data_imported = True

        # disable the next button in case it has been enabled during a previous import of another dataset
        self.pushButtonNext.setEnabled(False)

    def setup_column_assignment(self):
        """
        Creates a Label and Combo Box for each column of the training dataset
        and adds these to the page
        """
        # empty the col selection in case a second dataset is imported
        self.__col_selection = []
        self.reset_column_assignment()

        self.__col_names_train = self.__training_features.columns.to_list()

        for col in self.__col_names_train:
            row_of_layout = ColumnAssignment(col, self.__col_names_import)
            self.__col_selection.append(row_of_layout)

        for row in self.__col_selection:
            self.formLayout.addRow(row)

        # activate the confirm selection button
        self.pushButtonConfirmSel.setEnabled(True)

    def reset_column_assignment(self):
        """
        Clears the form layout containing the Column assignments
        and clears the list containing the ColumnAssignment Objects
        """
        # clear it in the beginning for when the column selection is updated (see 'next_page' method)
        self.__col_selection = []

        for i in reversed(range(self.formLayout.count())):
            self.formLayout.itemAt(i).widget().setParent(None)

    def get_selections(self):
        """
        Gets all pairs of training columns and corresponding imported columns
        """
        self.__column_assignment = []

        for layout_row in self.__col_selection:
            training_col, data_col = layout_row.get_information()
            assignment = (training_col, data_col)

            self.__column_assignment.append(assignment)

        # check for duplicates
        duplicates_present, duplicates = self.duplicates_in_selection()

        if duplicates_present:
            warning_text = "Duplicates found in assignment:"
            for duplicate in duplicates:
                warning_text += "\n %s" % duplicate

            QMessageBox.critical(self, "Column assignment failed",
                                 warning_text)

            self.__column_assignment = []

        else:
            QMessageBox.information(self, "Confirmed", "Column assignment confirmed!")
            # Activate the button to continue
            self.pushButtonNext.setEnabled(True)

    def duplicates_in_selection(self):
        """
        Checks whether a column from import has been assigned to multiple training columns
        :return:
        contains_doubles: bool; duplicates: list of duplicates
        """
        contains_duplicates = False
        seen = set()
        duplicates = []

        for assignment in self.__column_assignment:
            name = assignment[1]
            if name not in seen:
                seen.add(name)
            else:
                contains_duplicates = True
                duplicates.append(name)

        return contains_duplicates, duplicates

    def prepare_dataset_for_label(self):
        """
        Transforms the training and imported dataset into one-hot encoded form.
        """
        self.rename_columns_import()

        if self.check_categorical_columns():
            self.data_to_one_hot()
            self.tableOheImport.setModel(TableModel(np.round(self.__imported_one_hot, 2)))
            self.pushButtonNext.setEnabled(True)
        else:
            QMessageBox.critical(self, "Transformation failed",
                                 "The categorical columns differ between the imported and training dataset."
                                 " Please check the column assignment.")

    def rename_columns_import(self):
        """
        Updates the column names of the imported dataset with the corresponding names from the training data.
        The updates dataset is saved in __imported_data_adjusted
        """
        col_assignment_dict = {}
        for pair in self.__column_assignment:
            col_assignment_dict[pair[1]] = pair[0]

        self.__imported_data_adjusted = self.__imported_data.rename(columns=col_assignment_dict)

    def check_categorical_columns(self):
        """
        checks whether the categorical columns from the training and imported data are the same.
        :return:
        True: categorical columns match; False: cat. columns do not match
        """
        import_numeric_cols = self.__imported_data_adjusted._get_numeric_data().columns
        self.__import_categorical_cols = list(set(self.__imported_data_adjusted.columns) - set(import_numeric_cols))

        train_numeric_cols = self.__training_features._get_numeric_data().columns
        self.__training_categorical_cols = list(set(self.__training_features.columns) - set(train_numeric_cols))

        if self.__import_categorical_cols == self.__training_categorical_cols:
            return True
        else:
            return False

    def data_to_one_hot(self):
        """
        Transforms the imported dataset into one-hot encoded form.
        """
        self.__imported_one_hot = pd.get_dummies(self.__imported_data_adjusted)

        col_missing_in_one_hot = []
        # finds all columns of the one hot encoded imported dataset that are missing
        # compared to the one hot encoded training data
        for cat_column in self.__training_categorical_cols:
            # unique values of the current categorical column in the training dataset
            unique_values_train = self.__training_features[cat_column].unique()
            unique_values_import = self.__imported_data_adjusted[cat_column].unique()

            elements_not_in_import_col = np.setdiff1d(unique_values_train, unique_values_import)

            if len(elements_not_in_import_col) != 0:
                for element in elements_not_in_import_col:
                    element = cat_column + "_" + element
                    col_missing_in_one_hot.append(element)

        # add the missing columns to the one hot encoded import dataset filled with 0
        for col in col_missing_in_one_hot:
            self.__imported_one_hot[col] = 0

        # drop columns one hot encoded import data that are not in the one hot encoded training data
        columns_to_drop = np.setdiff1d(self.__imported_one_hot.columns, self.__training_features_one_hot.columns)
        self.__imported_one_hot.drop(columns_to_drop, axis=1)

        # rearrange column sequence to match the one from the one hot encoded training data
        self.__imported_one_hot = self.__imported_one_hot[self.__training_features_one_hot.columns]

        self.remove_weak_features()

    def remove_weak_features(self):
        """
        If a recursive feature elimination was performed when training the model:
        Drops unimportant features from the imported dataset.
        """
        important_features = self.__training_features_one_hot.columns
        if len(important_features) != 0:
            self.__imported_one_hot = self.__imported_one_hot[important_features]
            QMessageBox.information(self, "Transformation successful",
                                    "Imported dataset successfully transformed into one hot encoded form. "
                                    "Unimportant columns were dropped.")
        else:
            QMessageBox.information(self, "Transformation successful",
                                    "Imported dataset successfully transformed into one hot encoded form.")

    def start_labelling(self):
        """
        Predict the labels for each sample 100 times using a random subset of the training data.
        The 100 predictions for each sample are averaged to a final label depending on the mean.
        """
        self.pushButtonBack.setEnabled(False)
        self.pushButtonNext.setEnabled(False)
        self.pushStartLabel.setEnabled(False)
        self.tableLabelResults.setModel(None)

        self.progressBarLabel.setValue(0)
        self.textProgressLabel.setText("")

        worker = Worker(train_features=self.__training_features_one_hot,
                        train_targets=self.__training_target,
                        classifier=self.__active_classifier,
                        import_data=self.__imported_one_hot)
        worker.signals.progress.connect(self.update_text_browser)
        worker.signals.iteration.connect(self.update_progress_bar)
        worker.signals.predictions.connect(self.get_predictions)

        self.threadpool.start(worker)

    def update_text_browser(self, progress: str):
        """
        Shows the current operation done by the Worker in the textBrowser.
        :param progress: current operation
        """
        self.textProgressLabel.append(progress)

    def update_progress_bar(self, iteration: int):
        """
        Updates the progress bar
        :param iteration: current iteration of the labelling
        """
        self.progressBarLabel.setValue(iteration + 1)

    def get_predictions(self, predictions: pd.DataFrame):
        """
        Receives the predictions from the Worker, calculates the final prediction and shows the results.
        :param predictions: Predictions from all iterations
        """
        # calculate the mean value for each sample
        mean_predictions = predictions.mean(axis=1)

        # assign a final label based on the mean
        final_predictions = mean_predictions
        final_predictions.loc[final_predictions < 0.5] = 0
        final_predictions.loc[final_predictions >= 0.5] = 1
        final_predictions = final_predictions.astype("int")
        # combine all information into one dataframe
        self.__labelling_summary = pd.DataFrame({"result": final_predictions,
                                                 "mean": predictions.mean(axis=1),
                                                 "std": round(predictions.std(axis=1), 3)})

        self.tableLabelResults.setModel(TableModel(np.round(self.__labelling_summary, 3)))

        self.pushButtonSave.setEnabled(True)
        self.pushButtonBack.setEnabled(True)
        self.pushStartLabel.setEnabled(True)
        self.pushButtonNext.setEnabled(True)

    def save_results(self):
        now = datetime.datetime.now()
        path_save, _ = QFileDialog.getSaveFileName(self, "Save file", now.strftime("/home/labelled_%y_%m_%d_%H_%M_%S"), "CSV (*.csv *.CSV)")
        if path_save:
            self.__labelling_summary.to_csv(path_save)
            self.__was_exported = True

    def close_application(self):
        if not self.__was_exported:
            info_box = QMessageBox.question(self, "Close window?",
                                            "You did not export any data. Are you sure that you want to close the window?",
                                            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                            defaultButton=QMessageBox.StandardButton.No)
            if info_box == QMessageBox.StandardButton.No:
                return
        QApplication.instance().quit()

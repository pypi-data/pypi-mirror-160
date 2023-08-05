
import sys
import json as js
from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QFileDialog,
    QComboBox,
    QScrollArea,
    QGroupBox,
    QLineEdit,
)
from .movement_builder import (
    makeVerticalLine,
    makeGrid,
    makeHorizontalLine
)
import time
import pyqtgraph as pg


class SpatialExperimentGUI(QMainWindow):
    """
    This GUI is meant for generating and running spatial experiments at the 28-id beamline at NSLS II.
    """
    def __init__(self, SE28IdConfig={'my_config': {}, 'extra_md_experiment': {},
                                     'sample_dict': {}, 'scan_dict': {},
                                     'scans_completed': {}}, parent=None):
        """
        Initalizes the main window of the GUI and defults to a blank data set.
        """
        super(SpatialExperimentGUI, self).__init__(parent)
        self.SE28IdConfig = SE28IdConfig
        self.resize(1000, 800)
        self.mainbox = QWidget()
        self.setCentralWidget(self.mainbox)
        self.mainbox.setLayout(QVBoxLayout())
        self.topLayout = QHBoxLayout()
        self.mainbox.layout().addLayout(self.topLayout)
        self.loadBtn = QPushButton('Load', self)
        self.loadBtn.clicked.connect(self.loadJson)
        self.topLayout.addWidget(self.loadBtn)
        self.saveBtn = QPushButton('Save', self)
        self.saveBtn.clicked.connect(self.saveJson)
        self.topLayout.addWidget(self.saveBtn)
        self.my_configBtn = QPushButton('My config', self)
        self.my_configBtn.clicked.connect(self.viewMy_config)
        self.topLayout.addWidget(self.my_configBtn)
        self.experiment_mdBtn = QPushButton('Experiment md', self)
        self.experiment_mdBtn.clicked.connect(self.viewExp_md)
        self.topLayout.addWidget(self.experiment_mdBtn)
        self.sample_dictBtn = QPushButton('Samples', self)
        self.sample_dictBtn.clicked.connect(self.viewSample_dict)
        self.topLayout.addWidget(self.sample_dictBtn)
        self.scan_dictBtn = QPushButton('Scans', self)
        self.scan_dictBtn.clicked.connect(self.viewScan_dict)
        self.topLayout.addWidget(self.scan_dictBtn)
        self.scans_completedBtn = QPushButton('Scans Completed', self)
        # self.scans_completedBtn.clicked.connect(self.viewScans_completed)
        self.topLayout.addWidget(self.scans_completedBtn)
        self.startBtn = QPushButton("Start", self)
        self.startBtn.clicked.connect(self.unkillMe)
        # self.startBtn.clicked.connect(self.run_scans)
        self.startBtn.clicked.connect(self.update_plot)
        self.topLayout.addWidget(self.startBtn)
        self.killBtn = QPushButton("Stop", self)
        self.killBtn.clicked.connect(self.killMe)
        self.topLayout.addWidget(self.killBtn)
        self.killAllBtn = QPushButton("Stop All", self)
        self.killAllBtn.clicked.connect(self.killAllMe)
        self.topLayout.addWidget(self.killAllBtn)

        self.innerLayout = QHBoxLayout()
        self.mainbox.layout().addLayout(self.innerLayout)
        self.leftLayout = QVBoxLayout()
        self.rightLayout = QVBoxLayout()
        self.innerLayout.addLayout(self.leftLayout)
        self.innerLayout.addLayout(self.rightLayout)
        self.canvas = pg.GraphicsLayoutWidget()
        self.rightLayout.addWidget(self.canvas)

        # line plot
        self.mainplot = self.canvas.addPlot()
        self.mainplot.setLabel('left', "Grid_Y")
        self.mainplot.setLabel('bottom', "Grid_X")
        self.allpointsplot = self.mainplot.plot([1, 2, 3, 4, 5], [1, 2, 3, 4,
                                                5],
                                                pen=None, symbol='o',
                                                symbolPen=None, symbolSize=10,
                                                symbolBrush=('b'))
        self.activepointplot = self.mainplot.plot([1], [1], pen=None,
                                                  symbol='o', symbolPen=None,
                                                  symbolSize=10,
                                                  symbolBrush=('r'))
        self.currentPositions = [[(1, 1)]]
        try:
            self.currentScan = max([int(i) for i in self.SE28IdConfig['scans_completed'].keys()])
        except ValueError:
            self.currentScan = 0
        try:
            self.innerCount = self.SE28IdConfig['scans_completed'][str(self.currentScan)][1]
        except KeyError:
            self.innerCount = 0
        self.xr = 0
        self.yr = 0
        self.move_sleep = 0
# the following functions are not finished and will not run: start

    def _getMd(self, x: float, y: float) -> dict:
        """
        Adds metadata to each exposure.
        """
        md = {
            **self.SE28IdConfig['extra_md_experiment'],
            **self.extra_md_scan,
            **self.extra_md_sample,
            **self.SE28IdConfig['extra_md_experiment'],
            **{
                'Grid_X': x,
                'Grid_Y': y,
                'frame_acq_time': glbl['frame_acq_time'],
                'exposure_time': self.exposTime,
                'move_segment': self.moveSegment,
                'sample': self.currentSample,
            }
        }
        return md

    def _collectImageAt(self, x: float, y: float):
        """
        Collect one exposure.
        """
        yield from bps.mv(Grid_X, x, Grid_Y, y)
        yield from bps.sleep(self.moveSleep)
        self.xr = (yield from bps.rd(Grid_X))
        self.yr = (yield from bps.rd(Grid_Y))
        md = self._getMd(self.xr, self.yr)
        yield from bp.list_grid_scan([pe1c], Grid_Y, [y], Grid_X, [x], md=md)
        return

    def scanPlanGenerator(self, x, y):
        """
        Generate one exposure.
        expos_time: A float of the time in seconds an exposure will take.
        run_index: A list of integer indexes corisponding to the positions
            in the all_positions list. These are the positions that will be
            scanned over.
        extra_md_scan: A dictionary of additional metadata for this scan.
            Defaults to an empty dictionary.
        """

        yield from _configure_area_det(self.exposTime)
        yield from self._collectImageAt(x, y)
        return

    def runScan(self, spGenerator):
        """
        Do one xrun.
        """
        xrun(self.currentSampleIndex, spGenerator, user_config=self.SE28IdConfig['my_config'])
        print('exposure finished.\n')

    def setPowerOutput(self, x):
        """ give percentage output (0-100) """
        caput('XF:28ID1-ES{LS336:1-Out:3}Out:Man-SP', x)

    def darkCollection(self):
        """
        Generate one dark.
        """
        yield from take_dark()
        return

    def runDark(self):
        """
        Collect one dark.
        """
        darkPlan = self.darkCollection()
        self.runScan(darkPlan)

    def singleScan(self):
        """
        Single scan loop.
        """
        for sample in self.activeScan['samples'].keys():
            self.currentSample = sample
            self.extra_md_sample = self.SE28IdConfig['sample_dict'][sample]['extra_md_sample']
            self.currentSampleIndex = self.SE28IdConfig['sample_dict'][sample]['sample_index']
            for moveSeg in self.activeScan['samples'][sample]['move_segments'].keys():
                self.exposTime = self.activeScan['samples'][sample]['move_segments'][moveSeg][1]
                self.moveSleep = self.activeScan['samples'][sample]['move_segments'][moveSeg][0]
                self.moveSeg = moveSeg
                self.currentMoveSeg = self.SE28IdConfig['sample_dict'][sample]['move_segments'][moveSeg]
                if self.currentMoveSeg['segment_type'] == 'vertical':
                    allPositions = makeVerticalLine([i for i in self.currentMoveSeg['segment_values']])
                elif self.currentMoveSeg['segment_type'] == 'horizontal':
                    allPositions = makeHorizontalLine([i for i in self.currentMoveSeg['segment_values']])
                elif self.currentMoveSeg['segment_type'] == 'grid':
                    allPositions = makeGrid([i for i in self.currentMoveSeg['segment_values']])
                for pos in allPositions:
                    gen = self.scanPlanGenerator(pos[0], pos[1])
                    self.runScan(gen)

    def single_scan(self, sp_exp_generators):
        """
        Single scan loop.
        """
        if self.killAll:
            self.SE28IdConfig['scans_completed'][str(self.currentScan)] =\
                {'incomplete': self.innerCount,
                    'time_ran': time.time() - self.t0}
            return None
        if self.innerCount <= len(self.generators):
            self.run_scan(self.generators[self.innerCount][0], self.generators[self.innerCount][1])
            QtCore.QTimer.singleShot(1, self.single_scan)
            self.innerCount += 1
        else:
            print('Loop completed in ' + str(time.time() - self.t0) + ' seconds')
            QtCore.QTimer.singleShot(1, self.run_scans)
            self.currentScan += 1

    def time_scan_outer(self):
        """
        Outer loop of a time scan.
        """
        if self.kill:
            self.SE28IdConfig['scans_completed'][str(self.currentScan)] =\
                {'incomplete': 'all', 'time_ran': time.time() - self.t0}
            return None
        self.generators = self.makeGenerators()
        self.innerCount = 0

        if time.time() - self.t0 < self.activeScan['hold_time']:
            self.time_scan_inner()
        else:
            self.SE28IdConfig['scans_completed'][str(self.currentScan)] =\
                'complete'
            QtCore.QTimer.singleShot(1, self.run_scans)
            self.currentScan += 1

    def time_scan_inner(self):
        """
        Inner loop of a time scan.
        """
        if self.killAll:
            self.SE28IdConfig['scans_completed'][str(self.currentScan)] =\
                {'incomplete': self.innerCount,
                    'time_ran': time.time() - self.t0}
            return None
        if self.innerCount <= len(self.generators):
            self.run_scan(self.generators[self.innerCount][0], self.generators[self.innerCount][1])
            QtCore.QTimer.singleShot(1, self.time_scan_inner)
            self.innerCount += 1
        else:
            print('Loop completed in ' + str(time.time() - self.t0) + ' seconds')
            QtCore.QTimer.singleShot(self.activeScan['hold_between_time'] * 1000, self.time_scan_outer)

    def runScans(self):
        """
        run through all the scans in scan_dict.
        """
        if self.kill:
            return None
        try:
            self.activeScan = self.SE28IdConfig['scan_dict'][str(self.currentScan)]
            self.SE28IdConfig['scans_completed'][str(self.currentScan)] = ['started', 'incomplete']
        except KeyError:
            self.kill = True
            print('End of scans')
            return None
        if self.activeScan['scan_type'] == 'sleep':
            QtCore.QTimer.singleShot(self.activeScan['sleep_time'] * 1000, self.run_scans)
            self.SE28IdConfig['scans_completed'][str(self.currentScan)][1] = 'complete'
            self.currentScan += 1
        elif self.activeScan['scan_type'] == 'take_dark':
            self.run_dark()
            QtCore.QTimer.singleShot(1, self.run_scans)
            self.SE28IdConfig['scans_completed'][str(self.currentScan)][1] = 'complete'
            self.currentScan += 1
        elif self.activeScan['scan_type'] == 'set_power_output':
            self.set_power_output(self.currentScan['power'])
            QtCore.QTimer.singleShot(500, self.run_scans)
            self.SE28IdConfig['scans_completed'][str(self.currentScan)][1] = 'complete'
            self.currentScan += 1
        elif self.activeScan['scan_type'] == 'time_scan':
            self.t0 = time.time()
            self.time_scan()
        elif self.activeScan['scan_type'] == 'single_scan':
            self.generators = self.makeGenerators()
            self.innerCount = 0
            self.single_scan()

    def makeGenerators(self):
        """
        Make the generators for the currenct scan.
        """
        generators = []
        currentScanSamples = self.activeScan['samples']
        self.currentPositions = []
        for key in currentScanSamples.keys():
            posList = self.getMovement(key, currentScanSamples[key]['move_segment'])
            self.currentPositions.append[posList]
            for pos in posList:
                self.move_sleep = currentScanSamples[key]['move_segment']['move_sleep']
                generator = self.scanplan_generator(currentScanSamples[key]['exposure_time'],
                                                    pos[0], pos[1], currentScanSamples[key]['extra_md_scan'])
                generators.append((currentScanSamples[key]['sample_index'], generator))
        return generators

# end

    def clearLayout(self, layout):
        """
        Clear a layout in the GUI.
        """
        if layout is not None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget() is not None:
                    child.widget().deleteLater()
                elif child.layout() is not None:
                    self.clearLayout(child.layout())

    def getMovement(self, sample, move_segment):
        """
        get the movement of the current scan.
        """
        moveSeg = self.SE28IdConfig['sample_dict'][sample]['move_segments'][move_segment]
        inputs = moveSeg['inputs']
        if moveSeg['segment_type'] == 'vertical':
            return makeVerticalLine(inputs[0], inputs[1], inputs[2],
                                    inputs[3], inputs[4], inputs[5],
                                    inputs[6])
        elif moveSeg['segment_type'] == 'horizontal':
            return makeHorizontalLine(inputs[0], inputs[1], inputs[2],
                                      inputs[3], inputs[4], inputs[5],
                                      inputs[6])
        elif moveSeg['segment_type'] == 'grid':
            return makeGrid(inputs[0], inputs[1], inputs[2], inputs[3],
                            inputs[4], inputs[5], inputs[6], inputs[7],
                            inputs[8], inputs[9], inputs[10], inputs[11],
                            inputs[12], inputs[13])
        elif moveSeg['segment_type'] == 'list':
            return inputs

    def loadJson(self):
        """
        This function will get the address of the json file location and read it.
        """
        self.filename = QFileDialog.getOpenFileName(filter="json (*.json)")[0]
        print("File :", self.filename)
        if self.filename != '':
            with open(self.filename, 'r') as f:
                self.SE28IdConfig = js.load(f)
        else:
            print('No file selected.')

    def saveJson(self):
        """
        This function will get the address of the json file locationand save it.
        """
        self.filename = QFileDialog.getSaveFileName(filter="json (*.json)")[0]
        print("File :", self.filename)
        if self.filename != '':
            with open(self.filename, 'w') as f:
                js.dump(self.SE28IdConfig, f)
        else:
            print('No file name given.')

    def viewMy_config(self):
        """
        Set up the view window for My_config.
        """
        self.clearLayout(self.leftLayout)
        self.topInnerLayout = QHBoxLayout()
        self.leftLayout.addLayout(self.topInnerLayout)
        self.addNewKeyBtn = QPushButton('Add new', self)
        self.addNewKeyBtn.clicked.connect(self.addNewKeyMy_config)
        self.topInnerLayout.addWidget(self.addNewKeyBtn)
        self.updateMy_configBtn = QPushButton('Update', self)
        self.updateMy_configBtn.clicked.connect(self.updateMy_config)
        self.topInnerLayout.addWidget(self.updateMy_configBtn)
        self.mygroupbox = QGroupBox('User Config')
        self.myForm = QVBoxLayout()
        self.my_configLayoutList = []
        self.my_configKeyList = []
        self.my_configValueList = []
        self.my_configRemoveList = []
        for i, key in enumerate(self.SE28IdConfig['my_config'].keys()):
            self.my_configLayoutList.append(QHBoxLayout())
            self.my_configKeyList.append(QLineEdit(self))
            self.my_configKeyList[i].insert(str(key))
            self.my_configValueList.append(QLineEdit(self))
            self.my_configValueList[i].insert(str(self.SE28IdConfig['my_config'][key]))
            self.my_configRemoveList.append(QPushButton('Remove', self))
            self.my_configRemoveList[i].clicked.connect(lambda state, x=i: self.removeKeyMy_config(x))
            self.my_configLayoutList[i].addWidget(self.my_configKeyList[i])
            self.my_configLayoutList[i].addWidget(self.my_configValueList[i])
            self.my_configLayoutList[i].addWidget(self.my_configRemoveList[i])
            self.myForm.addLayout(self.my_configLayoutList[i])
        self.mygroupbox.setLayout(self.myForm)
        self.scroll = QScrollArea()
        self.scroll.setWidget(self.mygroupbox)
        self.scroll.setWidgetResizable(True)
        self.leftLayout.addWidget(self.scroll)

    def addNewKeyMy_config(self):
        """
        add a new key to the My_config window.
        """
        self.my_configLayoutList.append(QHBoxLayout())
        self.my_configKeyList.append(QLineEdit(self))
        self.my_configValueList.append(QLineEdit(self))
        self.my_configRemoveList.append(QPushButton('Remove', self))
        self.my_configRemoveList[-1].clicked.connect(lambda state, x=-1: self.removeKeyMy_config(x))
        self.my_configLayoutList[-1].addWidget(self.my_configKeyList[-1])
        self.my_configLayoutList[-1].addWidget(self.my_configValueList[-1])
        self.my_configLayoutList[-1].addWidget(self.my_configRemoveList[-1])
        self.myForm.addLayout(self.my_configLayoutList[-1])
        self.mygroupbox.setLayout(self.myForm)
        self.scroll.setWidget(self.mygroupbox)
        self.scroll.setWidgetResizable(True)

    def removeKeyMy_config(self, i):
        """
        Remove a key from the my config window.
        """
        del self.my_configKeyList[i]
        del self.my_configValueList[i]
        del self.my_configRemoveList[i]
        self.updateMy_config()
        self.viewMy_config()

    def updateMy_config(self):
        """
        Update the dictionary with the current information in the My_config window.
        """
        self.SE28IdConfig['my_config'] = {}
        for key, val in zip(self.my_configKeyList, self.my_configValueList):
            if val.text() == 'True':
                self.SE28IdConfig['my_config'][key.text()] = True
            elif val.text() == 'False':
                self.SE28IdConfig['my_config'][key.text()] = False
            else:
                self.SE28IdConfig['my_config'][key.text()] = val.text()
        self.viewMy_config()

    def viewExp_md(self):
        """
        Set up the view window for experiment metadata.
        """
        self.clearLayout(self.leftLayout)
        self.topInnerLayout = QHBoxLayout()
        self.leftLayout.addLayout(self.topInnerLayout)
        self.addNewKeyBtn = QPushButton('Add new', self)
        self.addNewKeyBtn.clicked.connect(self.addNewKeyExp_md)
        self.topInnerLayout.addWidget(self.addNewKeyBtn)
        self.updateExp_mdBtn = QPushButton('Update', self)
        self.updateExp_mdBtn.clicked.connect(self.updateExp_md)
        self.topInnerLayout.addWidget(self.updateExp_mdBtn)
        self.mygroupbox = QGroupBox('Experiment metadata')
        self.myForm = QVBoxLayout()
        self.Exp_mdLayoutList = []
        self.Exp_mdKeyList = []
        self.Exp_mdValueList = []
        self.Exp_mdRemoveList = []
        for i, key in enumerate(self.SE28IdConfig['extra_md_experiment'].keys()):
            self.Exp_mdLayoutList.append(QHBoxLayout())
            self.Exp_mdKeyList.append(QLineEdit(self))
            self.Exp_mdKeyList[i].insert(str(key))
            self.Exp_mdValueList.append(QLineEdit(self))
            self.Exp_mdValueList[i].insert(str(self.SE28IdConfig['extra_md_experiment'][key]))
            self.Exp_mdRemoveList.append(QPushButton('Remove', self))
            self.Exp_mdRemoveList[i].clicked.connect(lambda state, x=i: self.removeKeyExp_md(x))
            self.Exp_mdLayoutList[i].addWidget(self.Exp_mdKeyList[i])
            self.Exp_mdLayoutList[i].addWidget(self.Exp_mdValueList[i])
            self.Exp_mdLayoutList[i].addWidget(self.Exp_mdRemoveList[i])
            self.myForm.addLayout(self.Exp_mdLayoutList[i])
        self.mygroupbox.setLayout(self.myForm)
        self.scroll = QScrollArea()
        self.scroll.setWidget(self.mygroupbox)
        self.scroll.setWidgetResizable(True)
        self.leftLayout.addWidget(self.scroll)

    def addNewKeyExp_md(self):
        """
        add new key to experiment metadata
        """
        self.Exp_mdLayoutList.append(QHBoxLayout())
        self.Exp_mdKeyList.append(QLineEdit(self))
        self.Exp_mdValueList.append(QLineEdit(self))
        self.Exp_mdRemoveList.append(QPushButton('Remove', self))
        self.Exp_mdRemoveList[-1].clicked.connect(lambda state, x=-1: self.removeKeyExp_md(x))
        self.Exp_mdLayoutList[-1].addWidget(self.Exp_mdKeyList[-1])
        self.Exp_mdLayoutList[-1].addWidget(self.Exp_mdValueList[-1])
        self.Exp_mdLayoutList[-1].addWidget(self.Exp_mdRemoveList[-1])
        self.myForm.addLayout(self.Exp_mdLayoutList[-1])
        self.mygroupbox.setLayout(self.myForm)
        self.scroll.setWidget(self.mygroupbox)
        self.scroll.setWidgetResizable(True)

    def removeKeyExp_md(self, i):
        """
        remove a key from experiment metadata.
        """
        del self.Exp_mdKeyList[i]
        del self.Exp_mdValueList[i]
        del self.Exp_mdRemoveList[i]
        self.updateExp_md()
        self.viewExp_md()

    def updateExp_md(self):
        """
        update the experiment metadata with data currently in the view window.
        """
        self.SE28IdConfig['extra_md_experiment'] = {}
        for key, val in zip(self.Exp_mdKeyList, self.Exp_mdValueList):
            if val.text() == 'True':
                self.SE28IdConfig['extra_md_experiment'][key.text()] = True
            elif val.text() == 'False':
                self.SE28IdConfig['extra_md_experiment'][key.text()] = False
            else:
                self.SE28IdConfig['extra_md_experiment'][key.text()] = val.text()
        self.viewExp_md()

    def viewSample_dict(self):
        """
        set up the sample view window.
        """
        self.clearLayout(self.leftLayout)
        self. moveSegmentTypes = ["list", "vertical", "horizontal", "grid"]
        self.topInnerLayout = QHBoxLayout()
        self.leftLayout.addLayout(self.topInnerLayout)
        self.addNewKeyFill = QLineEdit()
        self.topInnerLayout.addWidget(self.addNewKeyFill)
        self.addNewKeyBtn = QPushButton('Add Sample', self)
        self.addNewKeyBtn.clicked.connect(self.addNewKeySample_dict)
        self.topInnerLayout.addWidget(self.addNewKeyBtn)
        self.updateSample_dictBtn = QPushButton('Update', self)
        self.updateSample_dictBtn.clicked.connect(self.updateSample_dict)
        self.topInnerLayout.addWidget(self.updateSample_dictBtn)
        self.mygroupbox = QGroupBox('Samples')
        self.myForm = QVBoxLayout()
        self.Sample_dictInfoDict = {}
        for key in self.SE28IdConfig['sample_dict'].keys():
            self.Sample_dictInfoDict[key] = {
                'sample_name': {}, 'sample_index': {}, 'extra_md_sample': {},
                'move_segments': {}, 'MD_add': {}, 'sample_remove': {},
                'segment_add': {}}
            self.Sample_dictInfoDict[key]['sample_name']['label'] = QLabel('Sample Name', self)
            self.Sample_dictInfoDict[key]['sample_name']['value'] = QLineEdit()
            self.Sample_dictInfoDict[key]['sample_name']['value'].insert(str(key))
            self.Sample_dictInfoDict[key]['sample_index']['label'] = QLabel('Sample Index', self)
            self.Sample_dictInfoDict[key]['sample_index']['value'] = QLineEdit()
            self.Sample_dictInfoDict[key]['sample_index']['value'].insert(
                str(self.SE28IdConfig['sample_dict'][key]['sample_index']))
            for key2 in self.SE28IdConfig['sample_dict'][key]['extra_md_sample'].keys():
                self.Sample_dictInfoDict[key]['extra_md_sample'][key2] = {}
                self.Sample_dictInfoDict[key]['extra_md_sample'][key2]['label'] = QLineEdit()
                self.Sample_dictInfoDict[key]['extra_md_sample'][key2]['label'].insert(str(key2))
                self.Sample_dictInfoDict[key]['extra_md_sample'][key2]['value'] = QLineEdit()
                self.Sample_dictInfoDict[key]['extra_md_sample'][key2]['value'].insert(
                    str(self.SE28IdConfig['sample_dict'][key]['extra_md_sample'][key2]))
                self.Sample_dictInfoDict[key]['extra_md_sample'][key2]['button'] = QPushButton('Remove MD', self)
                self.Sample_dictInfoDict[key]['extra_md_sample'][key2]['button'].clicked.connect(
                    lambda state, x=[key, key2]: self.removeSampleMD(x))
            for key2 in self.SE28IdConfig['sample_dict'][key]['move_segments'].keys():
                self.Sample_dictInfoDict[key]['move_segments'][key2] = {
                    'segment_name': {}, 'segment_type': {},
                    'segment_values': {}, 'segment_view': {},
                    'segment_remove': {}}
                self.Sample_dictInfoDict[key]['move_segments'][key2]['segment_name']['label'] =\
                    QLabel('Segment Name', self)
                self.Sample_dictInfoDict[key]['move_segments'][key2]['segment_name']['value'] =\
                    QLineEdit()
                self.Sample_dictInfoDict[key]['move_segments'][key2]['segment_name']['value'].insert(str(key2))
                self.Sample_dictInfoDict[key]['move_segments'][key2]['segment_type']['label'] =\
                    QLabel('Segment Type', self)
                self.Sample_dictInfoDict[key]['move_segments'][key2]['segment_type']['value'] =\
                    QComboBox()
                self.Sample_dictInfoDict[key]['move_segments'][key2]['segment_type']['value'].addItems(
                    self.moveSegmentTypes)
                self.Sample_dictInfoDict[key]['move_segments'][key2]['segment_type']['value'].setCurrentText(
                    self.SE28IdConfig['sample_dict'][key]['move_segments'][key2]['segment_type'])
                self.Sample_dictInfoDict[key]['move_segments'][key2]['segment_values']['label'] =\
                    QLabel('Segment Values', self)
                self.Sample_dictInfoDict[key]['move_segments'][key2]['segment_values']['value'] =\
                    QLineEdit()
                if self.SE28IdConfig['sample_dict'][key]['move_segments'][key2]['segment_type'] != 'list':
                    vals = str(
                        self.SE28IdConfig['sample_dict'][key]['move_segments'][key2]['segment_values']).replace(
                            '[', '')
                    vals = vals.replace(']', '')
                else:
                    vals = str(self.SE28IdConfig['sample_dict'][key]['move_segments'][key2]['segment_values'])
                    vals = vals[1::]
                    vals = vals[:-1:]
                    vals = vals.replace(',', ';')
                    vals = vals.replace('[', '(')
                    vals = vals.replace(']', ')')
                    vals = vals.replace('); (', '),(')

                self.Sample_dictInfoDict[key]['move_segments'][key2]['segment_values']['value'].insert(vals)
                self.Sample_dictInfoDict[key]['move_segments'][key2]['segment_view']['value'] =\
                    QPushButton('View', self)
                self.Sample_dictInfoDict[key]['move_segments'][key2]['segment_view']['value'].clicked.connect(
                    lambda state, x=[key, key2]: self.viewMoveSeg(x))
                self.Sample_dictInfoDict[key]['move_segments'][key2]['segment_remove']['value'] =\
                    QPushButton('Remove Segment', self)
                self.Sample_dictInfoDict[key]['move_segments'][key2]['segment_remove']['value'].clicked.connect(
                    lambda state, x=[key, key2]: self.removeMoveSeg(x))
            self.Sample_dictInfoDict[key]['MD_add']['value'] = QPushButton('Add MD', self)
            self.Sample_dictInfoDict[key]['MD_add']['value'].clicked.connect(lambda state, x=key: self.addMD(x))
            self.Sample_dictInfoDict[key]['segment_add']['label'] = QLineEdit()
            self.Sample_dictInfoDict[key]['segment_add']['value'] = QPushButton('Add move segment', self)
            self.Sample_dictInfoDict[key]['segment_add']['value'].clicked.connect(
                lambda state, x=key: self.addMoveSeg(x))
            self.Sample_dictInfoDict[key]['sample_remove']['value'] = QPushButton('Remove Sample', self)
            self.Sample_dictInfoDict[key]['sample_remove']['value'].clicked.connect(
                lambda state, x=key: self.removeSample(x))
        for key in self.Sample_dictInfoDict.keys():
            for key2 in self.Sample_dictInfoDict[key]['sample_name'].keys():
                self.myForm.addWidget(self.Sample_dictInfoDict[key]['sample_name'][key2])
            for key2 in self.Sample_dictInfoDict[key]['sample_index'].keys():
                self.myForm.addWidget(self.Sample_dictInfoDict[key]['sample_index'][key2])
            self.myForm.addWidget(QLabel('Extra MD Sample', self))
            for key2 in self.Sample_dictInfoDict[key]['MD_add'].keys():
                self.myForm.addWidget(self.Sample_dictInfoDict[key]['MD_add'][key2])
            for key2 in self.Sample_dictInfoDict[key]['extra_md_sample'].keys():
                for key3 in self.Sample_dictInfoDict[key]['extra_md_sample'][key2].keys():
                    self.myForm.addWidget(self.Sample_dictInfoDict[key]['extra_md_sample'][key2][key3])
            self.myForm.addWidget(QLabel('Move Segments', self))
            for key2 in self.Sample_dictInfoDict[key]['segment_add'].keys():
                self.myForm.addWidget(self.Sample_dictInfoDict[key]['segment_add'][key2])
            for key2 in self.Sample_dictInfoDict[key]['move_segments'].keys():
                for key3 in self.Sample_dictInfoDict[key]['move_segments'][key2].keys():
                    for key4 in self.Sample_dictInfoDict[key]['move_segments'][key2][key3].keys():
                        self.myForm.addWidget(self.Sample_dictInfoDict[key]['move_segments'][key2][key3][key4])
            for key2 in self.Sample_dictInfoDict[key]['sample_remove'].keys():
                self.myForm.addWidget(self.Sample_dictInfoDict[key]['sample_remove'][key2])

        self.mygroupbox.setLayout(self.myForm)
        self.scroll = QScrollArea()
        self.scroll.setWidget(self.mygroupbox)
        self.scroll.setWidgetResizable(True)
        self.leftLayout.addWidget(self.scroll)

    def addMoveSeg(self, key):
        """
        add a move segment to a sample.
        """
        name = self.Sample_dictInfoDict[key]['segment_add']['label'].text()
        if name:
            self.SE28IdConfig['sample_dict'][key]['move_segments'][name] = {
                'segment_type': 'vertical',
                'segment_values': [0, 0, 0, 0, 0, 0, 0]}
        else:
            return None
        self.viewSample_dict()

    def addMD(self, key):
        """
        add metadata to a sample.
        """
        self.SE28IdConfig['sample_dict'][key]['extra_md_sample']['new_key'] = 'new_value'
        self.viewSample_dict()

    def viewMoveSeg(self, keys):
        """
        plot a move segment in the plot window.
        """
        typ = self.Sample_dictInfoDict[keys[0]]['move_segments'][keys[1]]['segment_type']['value'].currentText()
        values = self.Sample_dictInfoDict[keys[0]]['move_segments'][keys[1]]['segment_values']['value'].text()
        if typ == 'vertical':
            vals = values.split(',')
            self.currentPositions = makeVerticalLine(
                float(vals[0]), float(vals[1]), float(vals[2]), float(vals[3]),
                float(vals[4]), float(vals[5]), int(vals[6]))
            self.update_plot_single()
        if typ == 'horizontal':
            vals = values.split(',')
            self.currentPositions = makeHorizontalLine(
                float(vals[0]), float(vals[1]), float(vals[2]), float(vals[3]),
                float(vals[4]), float(vals[5]), int(vals[6]))
            self.update_plot_single()
        if typ == 'grid':
            vals = values.split(',')
            self.currentPositions = makeGrid(
                float(vals[0]), float(vals[1]), float(vals[2]), float(vals[3]),
                float(vals[4]), float(vals[5]), int(vals[6]), float(vals[7]),
                float(vals[8]), float(vals[9]), float(vals[10]),
                float(vals[11]), float(vals[12]), int(vals[13]))
            self.update_plot_single()
        if typ == 'list':
            vals = values.split(',')
            self.currentPositions = [
                (float(i.split(';')[0].replace('(', '')),
                    float(i.split(';')[1].replace(')', ''))) for i in vals]
            self.update_plot_single()

    def removeMoveSeg(self, keys):
        """
        remove a move segment from a sample.
        """
        del self.SE28IdConfig['sample_dict'][keys[0]]['move_segments'][keys[1]]
        self.viewSample_dict()

    def removeSample(self, key):
        """
        remove a sample.
        """
        del self.SE28IdConfig['sample_dict'][key]
        self.viewSample_dict()

    def removeSampleMD(self, keys):
        """
        remove a key from the sample metadata.
        """
        del self.SE28IdConfig['sample_dict'][keys[0]]['extra_md_sample'][keys[1]]
        self.viewSample_dict()

    def addNewKeySample_dict(self):
        """
        add a sample.
        """
        name = self.addNewKeyFill.text()
        if name:
            self.SE28IdConfig['sample_dict'][name] = {
                'sample_index': 0, 'extra_md_sample': {}, 'move_segments': {}}
        else:
            return None
        self.viewSample_dict()

    def updateSample_dict(self):
        """
        update the sample window.
        """
        for key in self.Sample_dictInfoDict.keys():
            if key != self.Sample_dictInfoDict[key]['sample_name']['value'].text():
                del self.SE28IdConfig['sample_dict'][key]
                name = self.Sample_dictInfoDict[key]['sample_name']['value'].text()
            else:
                name = key
            self.SE28IdConfig['sample_dict'][name] = {
                'sample_index': self.Sample_dictInfoDict[key]['sample_index']['value'].text(),
                'extra_md_sample': {}, 'move_segments': {}}
            for key2 in self.Sample_dictInfoDict[key]['extra_md_sample'].keys():
                if key2 != self.Sample_dictInfoDict[key]['extra_md_sample'][key2]['label'].text():
                    name2 = self.Sample_dictInfoDict[key]['extra_md_sample'][key2]['label'].text()
                else:
                    name2 = key2
                self.SE28IdConfig['sample_dict'][name]['extra_md_sample'][name2] =\
                    self.Sample_dictInfoDict[key]['extra_md_sample'][key2]['value'].text()
            for key2 in self.Sample_dictInfoDict[key]['move_segments'].keys():
                if key2 != self.Sample_dictInfoDict[key]['move_segments'][key2]['segment_name']['value'].text():
                    name2 = self.Sample_dictInfoDict[key]['move_segments'][key2]['segment_name']['value'].text()
                else:
                    name2 = key2
                self.SE28IdConfig['sample_dict'][name]['move_segments'][name2] = {
                    'segment_type': self.Sample_dictInfoDict[
                        key]['move_segments'][key2]['segment_type']['value'].currentText(),
                    'segment_values': []}
                if self.SE28IdConfig['sample_dict'][name]['move_segments'][name2]['segment_type'] != 'list':
                    vals = self.Sample_dictInfoDict[key]['move_segments'][key2]['segment_values']['value'].text()
                    vals = vals.split(',')
                    vals2 = []
                    for val in vals:
                        try:
                            vals2.append(int(val))
                        except ValueError:
                            vals2.append(float(val))
                    self.SE28IdConfig['sample_dict'][name]['move_segments'][name2]['segment_values'] = vals2
                else:
                    vals = self.Sample_dictInfoDict[key]['move_segments'][key2]['segment_values']['value'].text()
                    vals = vals.split(',')
                    vals = [
                        (float(i.split('; ')[0].replace('(', '')),
                            float(i.split('; ')[1].replace(')', ''))) for i in vals]
                    self.SE28IdConfig['sample_dict'][name]['move_segments'][name2]['segment_values'] = vals

    def viewScan_dict(self):
        """
        set up the view for the scans.
        """
        self.clearLayout(self.leftLayout)
        self.ScanTypes = [
            "sleep",
            "take_dark",
            "set_power_output",
            "time_scan",
            "single_scan"]
        self.topInnerLayout = QHBoxLayout()
        self.leftLayout.addLayout(self.topInnerLayout)
        self.addNewKeyFill = QComboBox()
        self.addNewKeyFill.addItems(self.ScanTypes)
        self.topInnerLayout.addWidget(self.addNewKeyFill)
        self.addNewKeyBtn = QPushButton('Add scan', self)
        self.addNewKeyBtn.clicked.connect(self.addNewKeyScan_dict)
        self.topInnerLayout.addWidget(self.addNewKeyBtn)
        self.updateScan_dictBtn = QPushButton('Update', self)
        self.updateScan_dictBtn.clicked.connect(self.updateScan_dict)
        self.topInnerLayout.addWidget(self.updateScan_dictBtn)
        self.mygroupbox = QGroupBox('Scans')
        self.myForm = QVBoxLayout()
        self.Scan_dictInfoDict = {}
        for key in self.SE28IdConfig['scan_dict'].keys():
            self.Scan_dictInfoDict[key] = {
                'scan_number': {},
                'scan_type': {},
                'scan_remove': {},
                'scan_run': {}}
            self.Scan_dictInfoDict[key]['scan_number']['label'] = QLabel('scan index', self)
            self.Scan_dictInfoDict[key]['scan_number']['value'] = QComboBox()
            self.Scan_dictInfoDict[key]['scan_number']['value'].addItems(
                [i for i in self.SE28IdConfig['scan_dict'].keys()])
            self.Scan_dictInfoDict[key]['scan_number']['value'].setCurrentText(key)
            self.Scan_dictInfoDict[key]['scan_number']['value'].currentTextChanged.connect(
                lambda state, x=key: self.changeScanPosition(x))
            self.Scan_dictInfoDict[key]['scan_type']['label'] = QLabel(
                'Scan Type: ' + self.SE28IdConfig['scan_dict'][key]['scan_type'], self)
            self.Scan_dictInfoDict[key]['scan_remove']['value'] = QPushButton('Remove Scan', self)
            self.Scan_dictInfoDict[key]['scan_remove']['value'].clicked.connect(
                lambda state, x=key: self.removeScan(x))
            self.Scan_dictInfoDict[key]['scan_run']['value'] = QPushButton('Test Scan', self)
            self.Scan_dictInfoDict[key]['scan_run']['value'].clicked.connect(
                lambda state, x=key: self.testScan(x))
            if self.SE28IdConfig['scan_dict'][key]['scan_type'] == 'sleep':
                self.Scan_dictInfoDict[key]['sleep_time'] = {}
                self.Scan_dictInfoDict[key]['sleep_time']['label'] = QLabel('Sleep Time', self)
                self.Scan_dictInfoDict[key]['sleep_time']['value'] = QLineEdit()
                self.Scan_dictInfoDict[key]['sleep_time']['value'].insert(
                    str(self.SE28IdConfig['scan_dict'][key]['sleep_time']))
            elif self.SE28IdConfig['scan_dict'][key]['scan_type'] == 'take_dark':
                pass
            elif self.SE28IdConfig['scan_dict'][key]['scan_type'] == 'set_power_output':
                self.Scan_dictInfoDict[key]['power'] = {}
                self.Scan_dictInfoDict[key]['power']['label'] = QLabel('Power', self)
                self.Scan_dictInfoDict[key]['power']['value'] = QLineEdit()
                self.Scan_dictInfoDict[key]['power']['value'].insert(
                    str(self.SE28IdConfig['scan_dict'][key]['power']))
            elif self.SE28IdConfig['scan_dict'][key]['scan_type'] == 'single_scan':
                self.Scan_dictInfoDict[key]['samples'] = {'add_sample': {}}
                self.Scan_dictInfoDict[key]['samples']['add_sample']['label'] = QComboBox()
                self.Scan_dictInfoDict[key]['samples']['add_sample']['label'].addItems(
                    [i for i in self.SE28IdConfig['sample_dict'].keys()])
                self.Scan_dictInfoDict[key]['samples']['add_sample']['value'] =\
                    QPushButton('Add sample', self)
                self.Scan_dictInfoDict[key]['samples']['add_sample']['value'].clicked.connect(
                    lambda state, x=key: self.addScanSample(x))
                self.Scan_dictInfoDict[key]['extra_md_scan'] = {'add_md': {}}
                self.Scan_dictInfoDict[key]['extra_md_scan']['add_md']['value'] =\
                    QPushButton('Add MD', self)
                self.Scan_dictInfoDict[key]['extra_md_scan']['add_md']['value'].clicked.connect(
                    lambda state, x=key: self.addExt_md_scan(x))
                for key2 in self.SE28IdConfig['scan_dict'][key]['samples'].keys():
                    self.Scan_dictInfoDict[key]['samples'][key2] = {
                        'name': {},
                        'move_segments': {'add_move_seg': {}},
                        'remove_sample': {}}
                    self.Scan_dictInfoDict[key]['samples'][key2]['name']['label'] =\
                        QLabel('Sample Name: ' + key2, self)
                    self.Scan_dictInfoDict[key]['samples'][key2]['remove_sample']['value'] =\
                        QPushButton('Remove sample', self)
                    self.Scan_dictInfoDict[key]['samples'][key2]['remove_sample']['value'].clicked.connect(
                        lambda state, x=[key, key2]: self.removeScanSample(x))
                    self.Scan_dictInfoDict[key]['samples'][key2][
                        'move_segments']['add_move_seg']['label'] = QComboBox()
                    self.Scan_dictInfoDict[key]['samples'][key2][
                        'move_segments']['add_move_seg']['label'].addItems(
                        [i for i in self.SE28IdConfig['sample_dict'][key2]['move_segments'].keys()])
                    self.Scan_dictInfoDict[key]['samples'][key2]['move_segments']['add_move_seg']['value'] =\
                        QPushButton('Add move segment', self)
                    self.Scan_dictInfoDict[key]['samples'][key2][
                        'move_segments']['add_move_seg']['value'].clicked.connect(
                        lambda state, x=[key, key2]: self.addScanMoveSeg(x))
                    for key3 in self.SE28IdConfig['scan_dict'][key]['samples'][key2]['move_segments'].keys():
                        self.Scan_dictInfoDict[key]['samples'][key2]['move_segments'][key3] = {
                            'name': {},
                            'move_sleep': {},
                            'expos_time': {},
                            'remove_move_seg': {}}
                        self.Scan_dictInfoDict[key]['samples'][key2][
                            'move_segments'][key3]['name']['label'] =\
                            QLabel('Move segment name: ' + key3, self)
                        self.Scan_dictInfoDict[key]['samples'][key2][
                            'move_segments'][key3]['move_sleep']['label'] = QLabel('Move sleep', self)
                        self.Scan_dictInfoDict[key]['samples'][key2][
                            'move_segments'][key3]['move_sleep']['value'] = QLineEdit()
                        self.Scan_dictInfoDict[key]['samples'][key2][
                            'move_segments'][key3]['move_sleep']['value'].insert(
                            str(self.SE28IdConfig['scan_dict'][key]['samples'][key2]['move_segments'][key3][0]))
                        self.Scan_dictInfoDict[key]['samples'][key2][
                            'move_segments'][key3]['expos_time']['label'] = QLabel('Exposure time', self)
                        self.Scan_dictInfoDict[key]['samples'][key2][
                            'move_segments'][key3]['expos_time']['value'] = QLineEdit()
                        self.Scan_dictInfoDict[key]['samples'][key2][
                            'move_segments'][key3]['expos_time']['value'].insert(
                            str(self.SE28IdConfig['scan_dict'][key]['samples'][key2]['move_segments'][key3][1]))
                        self.Scan_dictInfoDict[key]['samples'][key2][
                            'move_segments'][key3]['remove_move_seg']['value'] =\
                            QPushButton('Remove move segment', self)
                        self.Scan_dictInfoDict[key]['samples'][key2][
                            'move_segments'][key3]['remove_move_seg']['value'].clicked.connect(
                            lambda state, x=[key, key2, key3]: self.removeScanMoveSeg(x))
                for key2 in self.SE28IdConfig['scan_dict'][key]['extra_md_scan'].keys():
                    self.Scan_dictInfoDict[key]['extra_md_scan'][key2] = {
                        'key': {},
                        'val': {},
                        'remove_md': {}}
                    self.Scan_dictInfoDict[key]['extra_md_scan'][key2]['key']['label'] = QLabel('key', self)
                    self.Scan_dictInfoDict[key]['extra_md_scan'][key2]['key']['value'] = QLineEdit()
                    self.Scan_dictInfoDict[key]['extra_md_scan'][key2]['key']['value'].insert(key2)
                    self.Scan_dictInfoDict[key]['extra_md_scan'][key2]['val']['label'] = QLabel('value', self)
                    self.Scan_dictInfoDict[key]['extra_md_scan'][key2]['val']['value'] = QLineEdit()
                    self.Scan_dictInfoDict[key]['extra_md_scan'][key2]['val']['value'].insert(
                        str(self.SE28IdConfig['scan_dict'][key]['extra_md_scan'][key2]))
                    self.Scan_dictInfoDict[key]['extra_md_scan'][key2]['remove_md']['value'] =\
                        QPushButton('Remove md', self)
                    self.Scan_dictInfoDict[key]['extra_md_scan'][key2]['remove_md']['value'].clicked.connect(
                        lambda state, x=[key, key2]: self.removeExt_md_scan(x))
            elif self.SE28IdConfig['scan_dict'][key]['scan_type'] == 'time_scan':
                self.Scan_dictInfoDict[key]['total_time'] = {}
                self.Scan_dictInfoDict[key]['total_time']['label'] = QLabel('Total time')
                self.Scan_dictInfoDict[key]['total_time']['value'] = QLineEdit()
                self.Scan_dictInfoDict[key]['total_time']['value'].insert(
                    str(self.SE28IdConfig['scan_dict'][key]['times'][0]))
                self.Scan_dictInfoDict[key]['between_time'] = {}
                self.Scan_dictInfoDict[key]['between_time']['label'] = QLabel('Between time')
                self.Scan_dictInfoDict[key]['between_time']['value'] = QLineEdit()
                self.Scan_dictInfoDict[key]['between_time']['value'].insert(
                    str(self.SE28IdConfig['scan_dict'][key]['times'][1]))
                self.Scan_dictInfoDict[key]['samples'] = {'add_sample': {}}
                self.Scan_dictInfoDict[key]['samples']['add_sample']['label'] = QComboBox()
                self.Scan_dictInfoDict[key]['samples']['add_sample']['label'].addItems(
                    [i for i in self.SE28IdConfig['sample_dict'].keys()])
                self.Scan_dictInfoDict[key]['samples']['add_sample']['value'] =\
                    QPushButton('Add sample', self)
                self.Scan_dictInfoDict[key]['samples']['add_sample']['value'].clicked.connect(
                    lambda state, x=key: self.addScanSample(x))
                self.Scan_dictInfoDict[key]['extra_md_scan'] = {'add_md': {}}
                self.Scan_dictInfoDict[key]['extra_md_scan']['add_md']['value'] =\
                    QPushButton('Add MD', self)
                self.Scan_dictInfoDict[key]['extra_md_scan']['add_md']['value'].clicked.connect(
                    lambda state, x=key: self.addExt_md_scan(x))
                for key2 in self.SE28IdConfig['scan_dict'][key]['samples'].keys():
                    self.Scan_dictInfoDict[key]['samples'][key2] = {
                        'name': {},
                        'move_segments': {'add_move_seg': {}},
                        'remove_sample': {}}
                    self.Scan_dictInfoDict[key]['samples'][key2]['name']['label'] =\
                        QLabel('Sample Name: ' + key2, self)
                    self.Scan_dictInfoDict[key]['samples'][key2]['remove_sample']['value'] =\
                        QPushButton('Remove sample', self)
                    self.Scan_dictInfoDict[key]['samples'][key2]['remove_sample']['value'].clicked.connect(
                        lambda state, x=[key, key2]: self.removeScanSample(x))
                    self.Scan_dictInfoDict[key]['samples'][key2][
                        'move_segments']['add_move_seg']['label'] = QComboBox()
                    self.Scan_dictInfoDict[key]['samples'][key2][
                        'move_segments']['add_move_seg']['label'].addItems(
                        [i for i in self.SE28IdConfig['sample_dict'][key2]['move_segments'].keys()])
                    self.Scan_dictInfoDict[key]['samples'][key2]['move_segments']['add_move_seg']['value'] =\
                        QPushButton('Add move segment', self)
                    self.Scan_dictInfoDict[key]['samples'][key2][
                        'move_segments']['add_move_seg']['value'].clicked.connect(
                        lambda state, x=[key, key2]: self.addScanMoveSeg(x))
                    for key3 in self.SE28IdConfig['scan_dict'][key]['samples'][key2]['move_segments'].keys():
                        self.Scan_dictInfoDict[key]['samples'][key2]['move_segments'][key3] = {
                            'name': {},
                            'move_sleep': {},
                            'expos_time': {},
                            'remove_move_seg': {}}
                        self.Scan_dictInfoDict[key]['samples'][key2]['move_segments'][key3]['name']['label'] =\
                            QLabel('Move segment name: ' + key3, self)
                        self.Scan_dictInfoDict[key]['samples'][key2][
                            'move_segments'][key3]['move_sleep']['label'] =\
                            QLabel('Move sleep', self)
                        self.Scan_dictInfoDict[key]['samples'][key2][
                            'move_segments'][key3]['move_sleep']['value'] = QLineEdit()
                        self.Scan_dictInfoDict[key]['samples'][key2][
                            'move_segments'][key3]['move_sleep']['value'].insert(
                            str(self.SE28IdConfig['scan_dict'][key]['samples'][key2]['move_segments'][key3][0]))
                        self.Scan_dictInfoDict[key]['samples'][key2][
                            'move_segments'][key3]['expos_time']['label'] =\
                            QLabel('Exposure time', self)
                        self.Scan_dictInfoDict[key]['samples'][key2][
                            'move_segments'][key3]['expos_time']['value'] = QLineEdit()
                        self.Scan_dictInfoDict[key]['samples'][key2][
                            'move_segments'][key3]['expos_time']['value'].insert(
                                str(self.SE28IdConfig['scan_dict'][key]['samples'][key2][
                                    'move_segments'][key3][1]))
                        self.Scan_dictInfoDict[key]['samples'][key2][
                            'move_segments'][key3]['remove_move_seg']['value'] =\
                            QPushButton('Remove move segment', self)
                        self.Scan_dictInfoDict[key]['samples'][key2][
                            'move_segments'][key3]['remove_move_seg']['value'].clicked.connect(
                                lambda state, x=[key, key2, key3]: self.removeScanMoveSeg(x))
                for key2 in self.SE28IdConfig['scan_dict'][key]['extra_md_scan'].keys():
                    self.Scan_dictInfoDict[key]['extra_md_scan'][key2] = {
                        'key': {},
                        'val': {},
                        'remove_md': {}}
                    self.Scan_dictInfoDict[key]['extra_md_scan'][key2]['key']['label'] =\
                        QLabel('key', self)
                    self.Scan_dictInfoDict[key]['extra_md_scan'][key2]['key']['value'] = QLineEdit()
                    self.Scan_dictInfoDict[key]['extra_md_scan'][key2]['key']['value'].insert(key2)
                    self.Scan_dictInfoDict[key]['extra_md_scan'][key2]['val']['label'] = QLabel('value', self)
                    self.Scan_dictInfoDict[key]['extra_md_scan'][key2]['val']['value'] = QLineEdit()
                    self.Scan_dictInfoDict[key]['extra_md_scan'][key2]['val']['value'].insert(
                        str(self.SE28IdConfig['scan_dict'][key]['extra_md_scan'][key2]))
                    self.Scan_dictInfoDict[key]['extra_md_scan'][key2]['remove_md']['value'] =\
                        QPushButton('Remove md', self)
                    self.Scan_dictInfoDict[key]['extra_md_scan'][key2]['remove_md']['value'].clicked.connect(
                        lambda state, x=[key, key2]: self.removeExt_md_scan(x))
        for key in self.Scan_dictInfoDict.keys():
            for key2 in self.Scan_dictInfoDict[key].keys():
                if key2 == 'scan_number':
                    self.myForm.addWidget(self.Scan_dictInfoDict[key][key2]['label'])
                    self.myForm.addWidget(self.Scan_dictInfoDict[key][key2]['value'])
                elif key2 == 'scan_remove':
                    self.myForm.addWidget(self.Scan_dictInfoDict[key][key2]['value'])
                elif key2 == 'scan_run':
                    self.myForm.addWidget(self.Scan_dictInfoDict[key][key2]['value'])
                elif key2 == 'scan_type':
                    self.myForm.addWidget(self.Scan_dictInfoDict[key][key2]['label'])
                    if 'take_dark' in self.Scan_dictInfoDict[key][key2]['label'].text():
                        continue
                    if 'sleep' in self.Scan_dictInfoDict[key][key2]['label'].text():
                        self.myForm.addWidget(self.Scan_dictInfoDict[key]['sleep_time']['label'])
                        self.myForm.addWidget(self.Scan_dictInfoDict[key]['sleep_time']['value'])
                    if 'set_power_output' in self.Scan_dictInfoDict[key][key2]['label'].text():
                        self.myForm.addWidget(self.Scan_dictInfoDict[key]['power']['label'])
                        self.myForm.addWidget(self.Scan_dictInfoDict[key]['power']['value'])
                    if 'single_scan' in self.Scan_dictInfoDict[key][key2]['label'].text():
                        self.myForm.addWidget(QLabel('Samples', self))
                        for key3 in self.Scan_dictInfoDict[key]['samples'].keys():
                            if key3 == 'add_sample':
                                self.myForm.addWidget(self.Scan_dictInfoDict[key][
                                    'samples'][key3]['label'])
                                self.myForm.addWidget(self.Scan_dictInfoDict[key][
                                    'samples'][key3]['value'])
                            else:
                                for key4 in self.Scan_dictInfoDict[key]['samples'][key3].keys():
                                    if key4 == 'name':
                                        self.myForm.addWidget(self.Scan_dictInfoDict[key][
                                            'samples'][key3][key4]['label'])
                                    elif key4 == 'remove_sample':
                                        self.myForm.addWidget(self.Scan_dictInfoDict[key][
                                            'samples'][key3][key4]['value'])
                                    elif key4 == 'move_segments':
                                        self.myForm.addWidget(QLabel('Move segments', self))
                                        for key5 in self.Scan_dictInfoDict[key]['samples'][key3][key4].keys():
                                            if key5 == 'add_move_seg':
                                                self.myForm.addWidget(self.Scan_dictInfoDict[key][
                                                    'samples'][key3][key4][key5]['label'])
                                                self.myForm.addWidget(self.Scan_dictInfoDict[key][
                                                    'samples'][key3][key4][key5]['value'])
                                            else:
                                                self.myForm.addWidget(self.Scan_dictInfoDict[key][
                                                    'samples'][key3][key4][key5]['name']['label'])
                                                self.myForm.addWidget(self.Scan_dictInfoDict[key][
                                                    'samples'][key3][key4][key5]['move_sleep']['label'])
                                                self.myForm.addWidget(self.Scan_dictInfoDict[key][
                                                    'samples'][key3][key4][key5]['move_sleep']['value'])
                                                self.myForm.addWidget(self.Scan_dictInfoDict[key][
                                                    'samples'][key3][key4][key5]['expos_time']['label'])
                                                self.myForm.addWidget(self.Scan_dictInfoDict[key][
                                                    'samples'][key3][key4][key5]['expos_time']['value'])
                                                self.myForm.addWidget(self.Scan_dictInfoDict[key][
                                                    'samples'][key3][key4][key5]['remove_move_seg']['value'])
                        self.myForm.addWidget(QLabel('Extra MD', self))
                        for key3 in self.Scan_dictInfoDict[key]['extra_md_scan'].keys():
                            if key3 == 'add_md':
                                self.myForm.addWidget(self.Scan_dictInfoDict[key][
                                    'extra_md_scan'][key3]['value'])
                            else:
                                self.myForm.addWidget(self.Scan_dictInfoDict[key][
                                    'extra_md_scan'][key3]['key']['label'])
                                self.myForm.addWidget(self.Scan_dictInfoDict[key][
                                    'extra_md_scan'][key3]['key']['value'])
                                self.myForm.addWidget(self.Scan_dictInfoDict[key][
                                    'extra_md_scan'][key3]['val']['label'])
                                self.myForm.addWidget(self.Scan_dictInfoDict[key][
                                    'extra_md_scan'][key3]['val']['value'])
                                self.myForm.addWidget(self.Scan_dictInfoDict[key][
                                    'extra_md_scan'][key3]['remove_md']['value'])
                    if 'time_scan' in self.Scan_dictInfoDict[key][key2]['label'].text():
                        self.myForm.addWidget(self.Scan_dictInfoDict[key]['total_time']['label'])
                        self.myForm.addWidget(self.Scan_dictInfoDict[key]['total_time']['value'])
                        self.myForm.addWidget(self.Scan_dictInfoDict[key]['between_time']['label'])
                        self.myForm.addWidget(self.Scan_dictInfoDict[key]['between_time']['value'])
                        self.myForm.addWidget(QLabel('Samples', self))
                        for key3 in self.Scan_dictInfoDict[key]['samples'].keys():
                            if key3 == 'add_sample':
                                self.myForm.addWidget(self.Scan_dictInfoDict[key]['samples'][key3]['label'])
                                self.myForm.addWidget(self.Scan_dictInfoDict[key]['samples'][key3]['value'])
                            else:
                                for key4 in self.Scan_dictInfoDict[key]['samples'][key3].keys():
                                    if key4 == 'name':
                                        self.myForm.addWidget(self.Scan_dictInfoDict[key][
                                            'samples'][key3][key4]['label'])
                                    elif key4 == 'remove_sample':
                                        self.myForm.addWidget(self.Scan_dictInfoDict[key][
                                            'samples'][key3][key4]['value'])
                                    elif key4 == 'move_segments':
                                        self.myForm.addWidget(QLabel('Move segments', self))
                                        for key5 in self.Scan_dictInfoDict[key]['samples'][key3][key4].keys():
                                            if key5 == 'add_move_seg':
                                                self.myForm.addWidget(self.Scan_dictInfoDict[key][
                                                    'samples'][key3][key4][key5]['label'])
                                                self.myForm.addWidget(self.Scan_dictInfoDict[key][
                                                    'samples'][key3][key4][key5]['value'])
                                            else:
                                                self.myForm.addWidget(self.Scan_dictInfoDict[key][
                                                    'samples'][key3][key4][key5]['name']['label'])
                                                self.myForm.addWidget(self.Scan_dictInfoDict[key][
                                                    'samples'][key3][key4][key5]['move_sleep']['label'])
                                                self.myForm.addWidget(self.Scan_dictInfoDict[key][
                                                    'samples'][key3][key4][key5]['move_sleep']['value'])
                                                self.myForm.addWidget(self.Scan_dictInfoDict[key][
                                                    'samples'][key3][key4][key5]['expos_time']['label'])
                                                self.myForm.addWidget(self.Scan_dictInfoDict[key][
                                                    'samples'][key3][key4][key5]['expos_time']['value'])
                                                self.myForm.addWidget(self.Scan_dictInfoDict[key][
                                                    'samples'][key3][key4][key5]['remove_move_seg']['value'])
                        self.myForm.addWidget(QLabel('Extra MD', self))
                        for key3 in self.Scan_dictInfoDict[key]['extra_md_scan'].keys():
                            if key3 == 'add_md':
                                self.myForm.addWidget(self.Scan_dictInfoDict[key]['extra_md_scan'][key3]['value'])
                            else:
                                self.myForm.addWidget(self.Scan_dictInfoDict[key][
                                    'extra_md_scan'][key3]['key']['label'])
                                self.myForm.addWidget(self.Scan_dictInfoDict[key][
                                    'extra_md_scan'][key3]['key']['value'])
                                self.myForm.addWidget(self.Scan_dictInfoDict[key][
                                    'extra_md_scan'][key3]['val']['label'])
                                self.myForm.addWidget(self.Scan_dictInfoDict[key][
                                    'extra_md_scan'][key3]['val']['value'])
                                self.myForm.addWidget(self.Scan_dictInfoDict[key][
                                    'extra_md_scan'][key3]['remove_md']['value'])
        self.mygroupbox.setLayout(self.myForm)
        self.scroll = QScrollArea()
        self.scroll.setWidget(self.mygroupbox)
        self.scroll.setWidgetResizable(True)
        self.leftLayout.addWidget(self.scroll)

    def updateScan_dict(self):
        """
        update the scan window.
        """
        for key in self.Scan_dictInfoDict.keys():
            if self.SE28IdConfig['scan_dict'][key]['scan_type'] == 'take_dark':
                continue
            elif self.SE28IdConfig['scan_dict'][key]['scan_type'] == 'sleep':
                self.SE28IdConfig['scan_dict'][key]['sleep_time'] =\
                    float(self.Scan_dictInfoDict[key]['sleep_time']['value'].text())
            elif self.SE28IdConfig['scan_dict'][key]['scan_type'] == 'set_power_output':
                self.SE28IdConfig['scan_dict'][key]['power'] =\
                    float(self.Scan_dictInfoDict[key]['power']['value'].text())
            elif self.SE28IdConfig['scan_dict'][key]['scan_type'] == 'single_scan':
                for key2 in self.SE28IdConfig['scan_dict'][key]['samples'].keys():
                    for key3 in self.SE28IdConfig['scan_dict'][key]['samples'][key2]['move_segments'].keys():
                        self.SE28IdConfig['scan_dict'][key]['samples'][key2]['move_segments'][key3] = [
                            float(self.Scan_dictInfoDict[key]['samples'][key2]['move_segments'][key3][
                                'move_sleep']['value'].text()), float(self.Scan_dictInfoDict[key][
                                    'samples'][key2]['move_segments'][key3]['expos_time']['value'].text())]
                mdKeyList = [i for i in self.SE28IdConfig['scan_dict'][key]['extra_md_scan'].keys()]
                for key2 in mdKeyList:
                    del self.SE28IdConfig['scan_dict'][key]['extra_md_scan'][key2]
                for key2 in self.Scan_dictInfoDict[key]['extra_md_scan'].keys():
                    if key2 != 'add_md':
                        self.SE28IdConfig['scan_dict'][key]['extra_md_scan'][self.Scan_dictInfoDict[key][
                            'extra_md_scan'][key2]['key']['value'].text()] =\
                            self.Scan_dictInfoDict[key]['extra_md_scan'][key2]['val']['value'].text()
            elif self.SE28IdConfig['scan_dict'][key]['scan_type'] == 'time_scan':
                self.SE28IdConfig['scan_dict'][key]['times'] = [
                    float(self.Scan_dictInfoDict[key]['total_time']['value'].text()),
                    float(self.Scan_dictInfoDict[key]['between_time']['value'].text())]
                for key2 in self.SE28IdConfig['scan_dict'][key]['samples'].keys():
                    for key3 in self.SE28IdConfig['scan_dict'][key]['samples'][key2]['move_segments'].keys():
                        self.SE28IdConfig['scan_dict'][key]['samples'][key2]['move_segments'][key3] =\
                            [float(self.Scan_dictInfoDict[key]['samples'][key2][
                                'move_segments'][key3]['move_sleep']['value'].text()),
                                float(self.Scan_dictInfoDict[key]['samples'][
                                    key2]['move_segments'][key3]['expos_time']['value'].text())]
                mdKeyList = [i for i in self.SE28IdConfig['scan_dict'][key]['extra_md_scan'].keys()]
                for key2 in mdKeyList:
                    del self.SE28IdConfig['scan_dict'][key]['extra_md_scan'][key2]
                for key2 in self.Scan_dictInfoDict[key]['extra_md_scan'].keys():
                    if key2 != 'add_md':
                        self.SE28IdConfig['scan_dict'][key]['extra_md_scan'][
                            self.Scan_dictInfoDict[key]['extra_md_scan'][key2][
                                'key']['value'].text()] = self.Scan_dictInfoDict[
                                    key]['extra_md_scan'][key2]['val']['value'].text()
        self.viewScan_dict()

    def addNewKeyScan_dict(self):
        """
        add a scan.
        """
        scanToAdd = self.addNewKeyFill.currentText()
        highest_num = 0
        for key in self.SE28IdConfig['scan_dict']:
            if int(key) > highest_num:
                highest_num = int(key)
        if scanToAdd == 'take_dark':
            self.SE28IdConfig['scan_dict'][str(highest_num + 1)] = {'scan_type': scanToAdd}
        elif scanToAdd == 'sleep':
            self.SE28IdConfig['scan_dict'][str(highest_num + 1)] = {
                'scan_type': scanToAdd,
                'sleep_time': 1}
        elif scanToAdd == 'set_power_output':
            self.SE28IdConfig['scan_dict'][str(highest_num + 1)] = {
                'scan_type': scanToAdd,
                'power': 0}
        elif scanToAdd == 'single_scan':
            self.SE28IdConfig['scan_dict'][str(highest_num + 1)] = {
                'scan_type': scanToAdd,
                'samples': {},
                'extra_md_scan': {}}
        elif scanToAdd == 'time_scan':
            self.SE28IdConfig['scan_dict'][str(highest_num + 1)] = {
                'scan_type': scanToAdd,
                'times': [1, 1],
                'samples': {},
                'extra_md_scan': {}}
        self.viewScan_dict()

    def removeScan(self, key):
        """
        remove a scan.
        """
        del self.SE28IdConfig['scan_dict'][key]
        sortedKeys = sorted(self.SE28IdConfig['scan_dict'].items())
        oldKeys = [i for i in self.SE28IdConfig['scan_dict'].keys()]
        for ikey in oldKeys:
            del self.SE28IdConfig['scan_dict'][ikey]
        for ikey in range(len(sortedKeys)):
            self.SE28IdConfig['scan_dict'][str(ikey)] = sortedKeys[ikey][1]
        self.viewScan_dict()

    def changeScanPosition(self, key):
        """
        change the order of a scan.
        """
        sortedKeys = sorted(self.SE28IdConfig['scan_dict'].items())
        oldKeys = [i for i in self.SE28IdConfig['scan_dict'].keys()]
        changedKeyNewValue = self.Scan_dictInfoDict[key]['scan_number']['value'].currentText()
        sortedKeys.insert(int(changedKeyNewValue), sortedKeys.pop(int(key)))
        for ikey in oldKeys:
            del self.SE28IdConfig['scan_dict'][ikey]
        for ikey in range(len(sortedKeys)):
            self.SE28IdConfig['scan_dict'][str(ikey)] = sortedKeys[ikey][1]
        self.viewScan_dict()

    def testScan(self, key):
        """
        run a scan.
        """
        print('ahh')

    def addExt_md_scan(self, key):
        """
        add scan metadata.
        """
        self.SE28IdConfig['scan_dict'][key]['extra_md_scan']['your_new_key'] = 'your_new_value'
        self.viewScan_dict()

    def removeExt_md_scan(self, keys):
        """
        remove scan metadata.
        """
        del self.SE28IdConfig['scan_dict'][keys[0]]['extra_md_scan'][keys[1]]
        self.viewScan_dict()

    def addScanSample(self, keys):
        """
        add a smple to a scan.
        """
        sampleToAdd = self.Scan_dictInfoDict[keys[0]]['samples']['add_sample']['label'].currentText()
        self.SE28IdConfig['scan_dict'][keys[0]]['samples'][sampleToAdd] = {'move_segments': {}}
        self.viewScan_dict()

    def removeScanSample(self, keys):
        """
        remove a sample from a scan.
        """
        del self.SE28IdConfig['scan_dict'][keys[0]]['samples'][keys[1]]
        self.viewScan_dict()

    def addScanMoveSeg(self, keys):
        """
        add a move segment to a scan.
        """
        segmentToAdd = self.Scan_dictInfoDict[keys[0]]['samples'][
            keys[1]]['move_segments']['add_move_seg']['label'].currentText()
        self.SE28IdConfig['scan_dict'][keys[0]]['samples'][keys[1]]['move_segments'][segmentToAdd] = [1, 1]
        self.viewScan_dict()

    def removeScanMoveSeg(self, keys):
        """
        remove a move segment from a scan.
        """
        del self.SE28IdConfig['scan_dict'][keys[0]]['samples'][keys[1]]['move_segments'][keys[2]]
        self.viewScan_dict()

    def killMe(self):
        """
        stop all outer loops.
        """
        self.kill = True
        print('Stopping')

    def killAllMe(self):
        """
        stop all inner and outer loops
        """
        self.kill = True
        self.killAll = True
        print('Stopping all')

    def unkillMe(self):
        """
        start the program.
        """
        self.kill = False
        self.killAll = False
        print('Starting')

    def update_plot_single(self):
        """
        update the plot window once.
        """
        self.allpoints_x = []
        self.allpoints_y = []
        for li in self.currentPositions:
            self.allpoints_x.append(li[0])
            self.allpoints_y.append(li[1])

        self.allpointsplot.setData(self.allpoints_x, self.allpoints_y)
        self.activepointplot.setData([self.currentPositions[0][0]], [self.currentPositions[0][1]])

    def update_plot(self):
        """
        Update the plot window continuously.
        """
        if self.kill:
            return None
        self.allpoints_x = []
        self.allpoints_y = []
        for li in self.currentPositions:
            self.allpoints_x.append(li[0])
            self.allpoints_y.append(li[1])

        self.allpointsplot.setData(self.allpoints_x, self.allpoints_y)
        self.activepointplot.setData([self.xr], [self.yr])
        QtCore.QTimer.singleShot(1000, self.update_plot)


def run_gui():
    """
    opens the gui.
    """
    app = QApplication(sys.argv)
    thisapp = SpatialExperimentGUI()
    thisapp.show()
    sys.exit(app.exec_())

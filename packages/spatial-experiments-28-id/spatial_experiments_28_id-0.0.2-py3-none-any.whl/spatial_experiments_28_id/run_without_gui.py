import json as js
import time
import matplotlib.pyplot as plt
from .movement_builder import (
    makeVerticalLine,
    makeGrid,
    makeHorizontalLine
)


class InputFileRunner():
    """
    This class alows a user to run an input file generated with
    SpatialExperimentGUI, outside of that GUI.
    """

    def __init__(self, SE28IdConfig, showImOnRun=False):
        """
        Initalize the class by loading an input file.
        """
        self.SE28IdConfig = {}
        self.loadFile = self.loadConfig(SE28IdConfig)
        self.currentScan = 0
        self.totalScans = len(self.SE28IdConfig['scan_dict'])
        self.currentSampleIndex = 0
        self.showImOnRun = showImOnRun
        if showImOnRun:
            plt.ion()
            self.fig, self.ax = plt.subplots()
            self.allP = self.ax.scatter([], [], label='All positions')
            self.currP = self.ax.scatter([], [], label='Current position')
            plt.title('current position')
            plt.xlabel('x (mm)')
            plt.ylabel('y (mm)')

    def __repr__(self):
        rep = str(self.SE28IdConfig)
        return rep

    def __str__(self):
        rep = str(self.SE28IdConfig)
        return rep

    def loadConfig(self, configName):
        """
        Load a json file with a premade SE28IdConfig.
        """
        with open(configName, 'r') as f:
            self.SE28IdConfig = js.load(f)
        return

    def saveConfig(self, configName):
        """
        save a input file as a json.
        """
        with open(configName, 'w') as f:
            js.dump(self.SE28IdConfig, f)
        return

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
        if self.showImOnRun:
            xs = [i[0] for i in self.allPositions]
            ys = [i[1] for i in self.allPositions]
            self.allP.set_xdata(xs, ys)
            self.currP.set_xdata([self.xr], [self.yr])
            self.ax.set_ylim(min(ys) - 10, max(ys) + 10)
            self.ax.set_xlim(min(xs) - 10, max(xs) + 10)
            self.allP.figure.canvas.draw()
            self.allP.figure.canvas.flush_events()
            self.currP.figure.canvas.draw()
            self.currP.figure.canvas.flush_events()

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
                    self.allPositions = makeVerticalLine([i for i in self.currentMoveSeg['segment_values']])
                elif self.currentMoveSeg['segment_type'] == 'horizontal':
                    self.allPositions = makeHorizontalLine([i for i in self.currentMoveSeg['segment_values']])
                elif self.currentMoveSeg['segment_type'] == 'grid':
                    self.allPositions = makeGrid([i for i in self.currentMoveSeg['segment_values']])
                elif self.currentMoveSeg['segment_type'] == 'list':
                    self.allPositions = self.currentMoveSeg['segment_values']
                for pos in self.allPositions:
                    gen = self.scanPlanGenerator(pos[0], pos[1])
                    self.runScan(gen)

    def timeScan(self):
        """
        time scan loop.
        """
        t0 = time.time()
        while True:
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
                    elif self.currentMoveSeg['segment_type'] == 'list':
                        allPositions = self.currentMoveSeg['segment_values']
                    for pos in allPositions:
                        gen = self.scanPlanGenerator(pos[0], pos[1])
                        self.runScan(gen)
            if time.time() - t0 >= self.activeScan['times'][0]:
                break
            time.sleep(self.activeScan['times'][1])

    def runInput(self):
        """
        run an input file.
        """
        for scan in list(range(self.totalScans))[self.currentScan:]:
            self.SE28IdConfig['scans_completed'][str(scan)] = ['unstarted', 'incomplete']
        for scan in list(range(self.totalScans))[self.currentScan:]:
            self.SE28IdConfig['scans_completed'][str(self.currentScan)][0] = 'started'
            try:
                self.activeScan = self.SE28IdConfig['scan_dict'][str(self.currentScan)]
                if self.activeScan['scan_type'] == 'take_dark':
                    self.runDark()
                elif self.activeScan['scan_type'] == 'sleep':
                    time.sleep(self.activeScan['sleep_time'])
                elif self.activeScan['scan_type'] == 'set_power_output':
                    self.setPowerOutput(self.activeScan['power'])
                elif self.activeScan['scan_type'] == 'single_scan':
                    self.extra_md_scan = self.activeScan['extra_md_scan']
                    self.singleScan()
                elif self.activeScan['scan_type'] == 'time_scan':
                    self.extra_md_scan = self.activeScan['extra_md_scan']
                    self.timeScan()
                self.SE28IdConfig['scans_completed'][str(self.currentScan)][1] = 'complete'
                self.currentScan += 1

            except KeyboardInterrupt:
                con = input("continue to next scan? [y/n]")
                if con == 'y' or 'Y':
                    print('continuing')
                    self.currentScan += 1
                    continue
                elif con == 'n' or 'N':
                    print('stopping')
                    break

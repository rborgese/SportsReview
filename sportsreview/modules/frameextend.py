# /*******************************************************************************
#  *   (c) Andrew Robinson (andrewjrobinson@gmail.com) 2014                      *
#  *                                                                             *
#  *  This file is part of SportsReview.                                         *
#  *                                                                             *
#  *  SportsReview is free software: you can redistribute it and/or modify       *
#  *  it under the terms of the GNU Lesser General Public License as published   *
#  *  by the Free Software Foundation, either version 3 of the License, or       *
#  *  (at your option) any later version.                                        *
#  *                                                                             *
#  *  SportsReview is distributed in the hope that it will be useful,            *
#  *  but WITHOUT ANY WARRANTY; without even the implied warranty of             *
#  *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the              *
#  *  GNU Lesser General Public License for more details.                        *
#  *                                                                             *
#  *  You should have received a copy of the GNU Lesser General Public License   *
#  *  along with SportsReview.  If not, see <http://www.gnu.org/licenses/>.      *
#  *                                                                             *
#  *******************************************************************************/
'''
Created on 09/04/2014
@author: Andrew Robinson
'''


from PyQt4.QtCore import pyqtSlot, QObject

class FrameExtend(QObject):
    '''Extends a framebuffer for a given period'''
    
    __CAPTURE_FRAME__ = False
    __PROCESS_FRAME__ = True
    __CAPTURE_GROUP__ = False
    __PROCESS_GROUP__ = False
    
    def __init__(self, settings, config):
        '''
        Extends a framebuffer for a given period
        
        @param settings: global settings object (from settings file)
        @param config: the specific configuration for this instance (from layout)
        '''
        QObject.__init__(self)
        
        self._settings = settings
        self._config = config
        
        self._settings.settingChanged.connect(self.settingChanged)
        self._extend = settings.getSetting("extend")
        
        self._framegroups = []
    
    @classmethod
    def getModule(cls, settings, config):
        '''Returns an instance of this module for the provided settings'''
        return cls(settings, config)
        
    def process(self, frame):
        '''
        Returns frame unchanged (but keeps a copy for configured timeperiod (settings file))
        
        @param frame: the incoming frame object
        @return: frame, the frame that was provided
        '''
        alivefgs = []
        for fg in self._framegroups:
            if frame.timestamp <= fg.endtime:
                fg.addFrame(frame)
                alivefgs.append(fg)
#             else:
#                 print "FrameExtend: %s frames" % fg._addcount
        self._framegroups = alivefgs
        
        return frame
    
    def giveFrames(self, framegroup):
        '''
        Get all the frames this module knows about which are used for pausing a video stream
        
        Note: this module doesn't initially load any frames into framegroup, instead it stores
        a reference to framegroup and adds incoming frames to it for a configured (setting) timeperiod
        
        @param framegroup: the framegroup object to store frames in.
        '''
        framegroup.endtime = framegroup.timestamp + self._extend
        self._framegroups.append(framegroup)
    
    @pyqtSlot(str,object)
    def settingChanged(self, name, value):
        if name == "extend":
            self._extend = float(value)

#end class FrameExtend

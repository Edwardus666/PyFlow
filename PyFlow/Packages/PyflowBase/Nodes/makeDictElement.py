from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *


class makeDictElement(NodeBase):
    def __init__(self, name):
        super(makeDictElement, self).__init__(name)
        self.bCacheEnabled = False
        self.key = self.createInputPin('key', 'AnyPin', structure=PinStructure.Single, constraint="1")
        self.value = self.createInputPin('value', 'AnyPin', structure=PinStructure.Multi, constraint="2")
        self.value.enableOptions(PinOptions.AllowAny)
        self.outArray = self.createOutputPin('out', 'AnyPin', defaultValue=(), structure=PinStructure.Single, constraint="2")
        self.outArray.enableOptions(PinOptions.AllowAny | PinOptions.DictElementSuported)
        self.outArray.onPinConnected.connect(self.outPinConnected)
        self.outArray.onPinDisconnected.connect(self.outPinDisConnected)
    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('AnyPin')
        helper.addOutputDataType('AnyPin')
        helper.addInputStruct(PinStructure.Single)
        helper.addInputStruct(PinStructure.Multi)
        helper.addOutputStruct(PinStructure.Single)
        return helper

    @staticmethod
    def category():
        return 'Array'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return 'Creates a Dict Element'

    def outPinDisConnected(self,inp):
        dictNode = inp.getDictNode([])
        if dictNode:
            for i in dictNode.arrayData.affected_by:
                dictItem = i.getDictElementNode([])
                if dictItem:
                    if dictItem.key in self.constraints[self.key.constraint]:
                        self.constraints[self.key.constraint].remove(dictItem.key)
                    if self.key in dictItem.constraints[self.key.constraint]:
                        dictItem.constraints[self.key.constraint].remove(self.key)

    def outPinConnected(self,inp):
        dictNode = inp.getDictNode([])
        if dictNode:
            for i in dictNode.arrayData.affected_by:
                dictItem = i.getDictElementNode([])
                if dictItem:
                    self.constraints[self.key.constraint].append(dictItem.key)
                    dictItem.constraints[self.key.constraint].append(self.key)
                    self.key.setType(dictItem.key.dataType)

    def compute(self, *args, **kwargs):
        self.outArray.setData(dictElement(self.key.getData(), self.value.getData()))

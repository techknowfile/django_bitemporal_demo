import { RootStoreBase } from "./RootStore.base"
import { types } from "mobx-state-tree";
import {FooTimestampModel} from "./FooTimestampModel";
import {BitemporalFooVersionModel} from "./BitemporalFooVersionModel";
import {values} from "mobx";
import {MSTGQLRef} from "mst-gql";

export const RootStore = RootStoreBase
  .props({
    startDate: types.Date,
    endDate: types.Date,
  })
  .volatile((self) => ({
  selectedItem: null,
}))
  .actions(self => ({
    // This is an auto-generated example action.
    log() {
      console.log(JSON.stringify(self))
    },
    setSelected(selection){
      console.log(selection)
      self.selectedItem = selection
    }
  }))
  .views(self => ({
    get days(){
      return Math.floor((self.endDate - self.startDate) / (1000*60*60*24))
    },
    get sliderMarks(){
      return values(self.bitemporalFooVersions).map((v, i) => ({
        value: i,
        label: v.timestamp.timestamp.substring(0, 10)
      }))
    }
  }))

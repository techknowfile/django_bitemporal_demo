import { FooVersionModelBase } from "./FooVersionModel.base"
import {getRoot} from "mobx-state-tree";


/* A graphql query fragment builders for FooVersionModel */
export { selectFromFooVersion, fooVersionModelPrimitives, FooVersionModelSelector } from "./FooVersionModel.base"

/**
 * FooVersionModel
 */
export const FooVersionModel = FooVersionModelBase
  .actions(self => ({
    // This is an auto-generated example action.
    log() {
      console.log(JSON.stringify(self))
    }
  }))
  .views(self => ({
    get width(){
      return (self.scoped_days / getRoot(self).days)*100 + "%"
    },
    get days(){
      return Math.floor((new Date(self.validEndDate + "T00:00:00") - new Date(self.validStartDate + "T00:00:00")) / (1000*60*60*24))
    },
    get scoped_days(){
      return Math.floor((Math.min(new Date(self.validEndDate + "T00:00:00"), getRoot(self).endDate) - Math.max(new Date(self.validStartDate + "T00:00:00"), getRoot(self).startDate)) / (1000*60*60*24))
    }
  }))

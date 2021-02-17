import { FooTimestampModelBase } from "./FooTimestampModel.base"


/* A graphql query fragment builders for FooTimestampModel */
export { selectFromFooTimestamp, fooTimestampModelPrimitives, FooTimestampModelSelector } from "./FooTimestampModel.base"

/**
 * FooTimestampModel
 */
export const FooTimestampModel = FooTimestampModelBase
  .actions(self => ({
    // This is an auto-generated example action.
    log() {
      console.log(JSON.stringify(self))
    }
  }))

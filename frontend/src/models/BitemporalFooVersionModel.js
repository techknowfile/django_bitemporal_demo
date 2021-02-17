import { BitemporalFooVersionModelBase } from "./BitemporalFooVersionModel.base"


/* A graphql query fragment builders for BitemporalFooVersionModel */
export { selectFromBitemporalFooVersion, bitemporalFooVersionModelPrimitives, BitemporalFooVersionModelSelector } from "./BitemporalFooVersionModel.base"

/**
 * BitemporalFooVersionModel
 */
export const BitemporalFooVersionModel = BitemporalFooVersionModelBase
  .actions(self => ({
    // This is an auto-generated example action.
    log() {
      console.log(JSON.stringify(self))
    }
  }))

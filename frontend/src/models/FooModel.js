import { FooModelBase } from "./FooModel.base"


/* A graphql query fragment builders for FooModel */
export { selectFromFoo, fooModelPrimitives, FooModelSelector } from "./FooModel.base"

/**
 * FooModel
 */
export const FooModel = FooModelBase
  .actions(self => ({
    // This is an auto-generated example action.
    log() {
      console.log(JSON.stringify(self))
    }
  }))

/* This is a mst-gql generated file, don't modify it manually */
/* eslint-disable */

import { types } from "mobx-state-tree"
import { MSTGQLRef, QueryBuilder } from "mst-gql"
import { ModelBase } from "./ModelBase"
import { FooModel } from "./FooModel"
import { FooModelSelector } from "./FooModel.base"


/**
 * FooTimestampBase
 * auto generated base class for the model FooTimestampModel.
 */
export const FooTimestampModelBase = ModelBase
  .named('FooTimestamp')
  .props({
    __typename: types.optional(types.literal("FooTimestamp"), "FooTimestamp"),
    id: types.identifier,
    identity: types.union(types.undefined, MSTGQLRef(types.late(() => FooModel))),
    timestamp: types.union(types.undefined, types.frozen()),
  })
  .views(self => ({
    get store() {
      return self.__getStore()
    }
  }))

export class FooTimestampModelSelector extends QueryBuilder {
  get id() { return this.__attr(`id`) }
  get timestamp() { return this.__attr(`timestamp`) }
  identity(builder) { return this.__child(`identity`, FooModelSelector, builder) }
}
export function selectFromFooTimestamp() {
  return new FooTimestampModelSelector()
}

export const fooTimestampModelPrimitives = selectFromFooTimestamp().timestamp

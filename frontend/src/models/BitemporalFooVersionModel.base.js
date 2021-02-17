/* This is a mst-gql generated file, don't modify it manually */
/* eslint-disable */

import { types } from "mobx-state-tree"
import { MSTGQLRef, QueryBuilder } from "mst-gql"
import { ModelBase } from "./ModelBase"
import { FooTimestampModel } from "./FooTimestampModel"
import { FooTimestampModelSelector } from "./FooTimestampModel.base"
import { FooVersionModel } from "./FooVersionModel"
import { FooVersionModelSelector } from "./FooVersionModel.base"


/**
 * BitemporalFooVersionBase
 * auto generated base class for the model BitemporalFooVersionModel.
 */
export const BitemporalFooVersionModelBase = ModelBase
  .named('BitemporalFooVersion')
  .props({
    __typename: types.optional(types.literal("BitemporalFooVersion"), "BitemporalFooVersion"),
    id: types.identifier,
    timestamp: types.union(types.undefined, types.null, MSTGQLRef(types.late(() => FooTimestampModel))),
    temporals: types.union(types.undefined, types.null, types.array(types.union(types.null, MSTGQLRef(types.late(() => FooVersionModel))))),
  })
  .views(self => ({
    get store() {
      return self.__getStore()
    }
  }))

export class BitemporalFooVersionModelSelector extends QueryBuilder {
  get id() { return this.__attr(`id`) }
  timestamp(builder) { return this.__child(`timestamp`, FooTimestampModelSelector, builder) }
  temporals(builder) { return this.__child(`temporals`, FooVersionModelSelector, builder) }
}
export function selectFromBitemporalFooVersion() {
  return new BitemporalFooVersionModelSelector()
}

export const bitemporalFooVersionModelPrimitives = selectFromBitemporalFooVersion()

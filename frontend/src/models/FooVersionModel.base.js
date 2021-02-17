/* This is a mst-gql generated file, don't modify it manually */
/* eslint-disable */

import { types } from "mobx-state-tree"
import { MSTGQLRef, QueryBuilder } from "mst-gql"
import { ModelBase } from "./ModelBase"
import { FooModel } from "./FooModel"
import { FooModelSelector } from "./FooModel.base"


/**
 * FooVersionBase
 * auto generated base class for the model FooVersionModel.
 */
export const FooVersionModelBase = ModelBase
  .named('FooVersion')
  .props({
    __typename: types.optional(types.literal("FooVersion"), "FooVersion"),
    id: types.identifier,
    validStartDate: types.union(types.undefined, types.frozen()),
    validEndDate: types.union(types.undefined, types.frozen()),
    sysStartDate: types.union(types.undefined, types.frozen()),
    sysEndDate: types.union(types.undefined, types.frozen()),
    identity: types.union(types.undefined, MSTGQLRef(types.late(() => FooModel))),
    value: types.union(types.undefined, types.number),
  })
  .views(self => ({
    get store() {
      return self.__getStore()
    }
  }))

export class FooVersionModelSelector extends QueryBuilder {
  get id() { return this.__attr(`id`) }
  get validStartDate() { return this.__attr(`validStartDate`) }
  get validEndDate() { return this.__attr(`validEndDate`) }
  get sysStartDate() { return this.__attr(`sysStartDate`) }
  get sysEndDate() { return this.__attr(`sysEndDate`) }
  get value() { return this.__attr(`value`) }
  identity(builder) { return this.__child(`identity`, FooModelSelector, builder) }
}
export function selectFromFooVersion() {
  return new FooVersionModelSelector()
}

export const fooVersionModelPrimitives = selectFromFooVersion().validStartDate.validEndDate.sysStartDate.sysEndDate.value

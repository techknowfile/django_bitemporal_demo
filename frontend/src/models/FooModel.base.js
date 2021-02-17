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
 * FooBase
 * auto generated base class for the model FooModel.
 */
export const FooModelBase = ModelBase
  .named('Foo')
  .props({
    __typename: types.optional(types.literal("Foo"), "Foo"),
    id: types.identifier,
    temporal: types.union(types.undefined, types.array(MSTGQLRef(types.late(() => FooVersionModel)))),
    versions: types.union(types.undefined, types.array(MSTGQLRef(types.late(() => FooTimestampModel)))),
  })
  .views(self => ({
    get store() {
      return self.__getStore()
    }
  }))

export class FooModelSelector extends QueryBuilder {
  get id() { return this.__attr(`id`) }
  temporal(builder) { return this.__child(`temporal`, FooVersionModelSelector, builder) }
  versions(builder) { return this.__child(`versions`, FooTimestampModelSelector, builder) }
}
export function selectFromFoo() {
  return new FooModelSelector()
}

export const fooModelPrimitives = selectFromFoo()

/* This is a mst-gql generated file, don't modify it manually */
/* eslint-disable */
import { types } from "mobx-state-tree"
import { MSTGQLStore, configureStoreMixin } from "mst-gql"

import { FooModel } from "./FooModel"
import { fooModelPrimitives, FooModelSelector } from "./FooModel.base"
import { FooVersionModel } from "./FooVersionModel"
import { fooVersionModelPrimitives, FooVersionModelSelector } from "./FooVersionModel.base"
import { FooTimestampModel } from "./FooTimestampModel"
import { fooTimestampModelPrimitives, FooTimestampModelSelector } from "./FooTimestampModel.base"
import { BitemporalFooVersionModel } from "./BitemporalFooVersionModel"
import { bitemporalFooVersionModelPrimitives, BitemporalFooVersionModelSelector } from "./BitemporalFooVersionModel.base"







/**
* Store, managing, among others, all the objects received through graphQL
*/
export const RootStoreBase = MSTGQLStore
  .named("RootStore")
  .extend(configureStoreMixin([['Foo', () => FooModel], ['FooVersion', () => FooVersionModel], ['FooTimestamp', () => FooTimestampModel], ['BitemporalFooVersion', () => BitemporalFooVersionModel]], ['Foo', 'FooVersion', 'FooTimestamp', 'BitemporalFooVersion'], "js"))
  .props({
    foos: types.optional(types.map(types.late(() => FooModel)), {}),
    fooVersions: types.optional(types.map(types.late(() => FooVersionModel)), {}),
    fooTimestamps: types.optional(types.map(types.late(() => FooTimestampModel)), {}),
    bitemporalFooVersions: types.optional(types.map(types.late(() => BitemporalFooVersionModel)), {})
  })
  .actions(self => ({
    queryHello(variables, options = {}) {
      return self.query(`query hello { hello }`, variables, options)
    },
    queryFoos(variables, resultSelector = fooModelPrimitives.toString(), options = {}) {
      return self.query(`query foos { foos {
        ${typeof resultSelector === "function" ? resultSelector(new FooModelSelector()).toString() : resultSelector}
      } }`, variables, options)
    },
    queryBitemporalFoos(variables, resultSelector = bitemporalFooVersionModelPrimitives.toString(), options = {}) {
      return self.query(`query bitemporalFoos { bitemporalFoos {
        ${typeof resultSelector === "function" ? resultSelector(new BitemporalFooVersionModelSelector()).toString() : resultSelector}
      } }`, variables, options)
    },
  }))

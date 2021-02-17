import logo from './logo.svg';
import './App.css';
import {useContext, useEffect} from "react";
import {StoreContext} from "./models";
import {values} from "mobx";
import {observer} from "mobx-react";
import Foo from "./components/Foo";
import {Slider} from "@material-ui/core";
import { makeStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';

function App() {
  const store = useContext(StoreContext)

  useEffect(() => {
    const query = store.queryBitemporalFoos({}, `
    __typename
    id
    timestamp {
      __typename
      id
      timestamp
    }
    temporals {
      __typename
      id
      validStartDate
      validEndDate
      sysStartDate
      sysEndDate
      value
    }
    `, )
    query.then(()=>console.log("Query complete"), ()=>console.log("Query failed!"))
    return () => {

    }
  }, [store])

  const onChange = (event, value) => {
    console.log("change")
    if (values(store.bitemporalFooVersions).length)
      store.setSelected(values(store.bitemporalFooVersions)[value])
  }
  return (
    <div style={{backgroundColor: "#EBD5EF", height: "100vh", padding: 50}}>
      <><Slider marks={store.sliderMarks}
                    defaultValue={0}
                    min={0}
                    max={values(store.bitemporalFooVersions).length - 1}
                    aria-labelledby="discrete-slider-restrict"
                    step={null}
                    valueLabelDisplay="on"
                    onChange={onChange}
          />
                    <Foo temporals={store.selectedItem ? store.selectedItem.temporals : null}/></>
    </div>
  );
}

export default observer(App);

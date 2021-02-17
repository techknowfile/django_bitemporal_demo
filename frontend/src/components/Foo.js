import {observer} from 'mobx-react'

const Foo = ({temporals}) => {
  console.log("asdfasdfadsf")
  if (temporals)
    return (
    <div style={{display: "flex"}}>
      {temporals.map(temporal =>
        <div style={{flex: temporal.width, display: "block", margin: 3, borderRadius: 5, backgroundColor: "#F7941F", textAlign: "center", padding: 5}}>
          {temporal.value}
        </div>
      )}
    </div>
  )
  else return (
    <div style={{display: "flex"}}>
      <div style={{flex: 1, display: "block", margin: 3, borderRadius: 5, backgroundColor: "gray", textAlign: "center", width: "100%", padding: 5}}>
          No Data
        </div>
    </div>)
}

export default observer(Foo)
import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import {RootStore, StoreContext} from "./models";
import { createHttpClient } from 'mst-gql'
import {values} from 'mobx'

const store = RootStore.create({
    startDate: new Date(2020, 0, 1),
    endDate: new Date(2020, 11, 31)
  },
  {
    gqlHttpClient: createHttpClient(
  'http://localhost:8000/graphql',
)
  })

ReactDOM.render(
  <StoreContext.Provider value={store}>
    <React.StrictMode>
      <App />
    </React.StrictMode>
  </StoreContext.Provider>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();

window.store = store
window.values = values
import React, { Component } from 'react';
import Inventory from './components/Inventory';
import './App.css';

const DEV_URL = 'http://localhost:8080/api/v1';
const API_URLS = {
  INVENTORY: DEV_URL + '/inventory'
};
const API_CODES = {
  SUCCESS: [
    280
    , 281
  ]
  , ERROR: [
    480
    , 490
  ]
};

class App extends Component {
  constructor(props) {
    super(props);
    this.fetchApi = this.fetchApi.bind(this);
    this.sendForm = this.sendForm.bind(this);
  }

  //  fetch() sends GET request to API
  //  Deserialize the fetched API data to a JS Object
  async fetchApi(API_URL) {
    const res = await fetch(API_URL);
    const api = await res.json();
    return api;
  };

  //  Send a form to API
  async sendForm(API_URL, request_method, data) {
    const res = await fetch(API_URL, {
      method: request_method
      , headers: {
        'Accept': 'application/json'
        , 'Content-Type': 'application/json'
      }
      , body: JSON.stringify(data)
    });

    const response = await res.json();
  };

  render() {
    return (
      <div className="App">
        <Inventory
          API_URL={API_URLS.INVENTORY}
          fetchInventory={this.fetchApi}
          sendForm={this.sendForm}
        />
      </div>
    );
  };
}

export default App;

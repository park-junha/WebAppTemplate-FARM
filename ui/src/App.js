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
    this.state = {
      new_item: {
        item_name: ''
        , quantity: 0
      }
    };
    this.handleChange = this.handleChange.bind(this);
    this.fetchApi = this.fetchApi.bind(this);
    this.sendForm = this.sendForm.bind(this);
  }

  //  Handle text input state change
  //  Preserve previous state to preserve all keys of state
  handleChange(event) {
    const target = event.target;
    this.setState(prevState => ({
      new_item: {
        ...prevState.new_item
        , item_name: target.value
      }
    }));
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
        <div>
          <span>
            <b>New Item: </b>
            <input
              type='text'
              value={this.state.new_item.item_name}
              onChange={this.handleChange}
            />
            <input
              type='button'
              onClick={() => {
                const data = {
                  ...this.state.new_item
                };
                this.sendForm(API_URLS.INVENTORY, 'POST', data);
              }}
              value='Create'
            />
          </span>
        </div>
        <br />
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

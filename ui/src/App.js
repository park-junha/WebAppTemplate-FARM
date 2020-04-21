import React, { Component } from 'react';
import Inventory from './components/Inventory';
import './App.css';

const DEV_URL = 'http://localhost:8080/api/v1';
const API_URLS = {
  ITEMS: DEV_URL + '/items',
  ITEM: DEV_URL + '/item/'
};
const API_CODES = {
  SUCCESS: {
    READ: 280,
    WRITE: 281
  }
};

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      new_item: {
        item_name: ''
        , quantity: 0
      }
      , item_added: false
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
    this.setState(prevState => ({
      ...prevState
      , item_added: false
    }));
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

    return response;
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
              onClick={async () => {
                const data = {
                  ...this.state.new_item
                };
                const res = await this.sendForm(API_URLS.ITEMS, 'POST', data);
                if (res.code === API_CODES.SUCCESS.WRITE) {
                  this.setState(prevState => ({
                    new_item: {
                      item_name: ''
                      , quantity: 0
                    }
                    , item_added: true
                  }));
                }
              }}
              value='Create'
            />
          </span>
        </div>
        <br />
        <Inventory
          API_URLS={API_URLS}
          API_CODES={API_CODES}
          item_added={this.state.item_added}
          fetchInventory={this.fetchApi}
          sendForm={this.sendForm}
        />
      </div>
    );
  };
}

export default App;

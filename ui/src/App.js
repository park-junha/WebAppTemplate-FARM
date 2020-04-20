import React, { Component } from 'react';
import Inventory from './components/Inventory';
import './App.css';

const DEV_URL = 'http://localhost:8080/api/v1';
const API_URLS = {
  INVENTORY: DEV_URL + '/inventory'
};

class App extends Component {
  //  Initialize state
  constructor(props) {
    super(props);
    this.state = {
      Inventory: []
    };
  }

  //  Get API data as soon as app loads
  componentDidMount() {
    this.fetchApi(API_URLS.INVENTORY);
  }

  //  fetch() sends GET request to API
  //  Deserialize the fetched API data to a JS Object
  async fetchApi(API_URL) {
    const res = await fetch(API_URL);
    const api = await res.json();
    this.setState({
      Inventory: api.result
    });
  }

  render() {
    return (
      <div className="App">
        <Inventory
          inventory={this.state.Inventory}
        />
      </div>
    );
  };
}

export default App;

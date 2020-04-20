import React, { Component } from 'react';
import Item from './Item';

export default class Inventory extends Component {
  //  Initialize state
  constructor(props) {
    super(props);
    this.state = {
      inventory: {}
    };
  }

  //  Get API data as soon as app loads
  async componentDidMount() {
    this.loadApi();
  }

  //  Load API data
  async loadApi () {
    const api = await this.props.fetchInventory(this.props.API_URL);
    this.setState({
      inventory: api.result
    });
  }

  render() {
    return (
      <div>
        {/* Reload inventory from API */}
        <div>
          <input
            type='button'
            value='Refresh'
            onClick={() => {
              this.setState({
                inventory: {}
              });
              this.loadApi();
            }}
          />
        <span>
          {this.props.item_added ? 'Item added to database. Please refresh.' : ''}
        </span>
        </div>
        {/* Iterate through keys of inventory API data */}
        {/* Managing updated state is easier with objects */}
        {Object.keys(this.state.inventory).map(uid => (
          <Item
            {...this.state.inventory[uid]}
            sendUpdate={async () => {
              const data = {
                ...this.state.inventory[uid]
              };
              const res = await this.props.sendForm(this.props.API_URL, 'PATCH', data);
              if (res.code === this.props.API_CODES.SUCCESS.WRITE) {
                return 'item-state-saved';
              }
            }}
            sendDelete={async () => {
              const data = {
                ...this.state.inventory[uid]
              };
              const res = await this.props.sendForm(this.props.API_URL, 'DELETE', data);
              if (res.code === this.props.API_CODES.SUCCESS.WRITE) {
                return 'item-state-deleted';
              }
            }}
            incrementItem={() => {
              var stateCopy = Object.assign({}, this.state);
              stateCopy.inventory[uid].quantity += 1;
              this.setState(stateCopy);
            }}
            decrementItem={() => {
              if (this.state.inventory[uid].quantity > 0) {
                var stateCopy = Object.assign({}, this.state);
                stateCopy.inventory[uid].quantity -= 1;
                this.setState(stateCopy);
              }
            }}
          />
        ))}
      </div>
    );
  };
}

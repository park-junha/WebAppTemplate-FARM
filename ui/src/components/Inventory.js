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
    const api = await this.props.fetchInventory(this.props.API_URL);
    this.setState({
      inventory: api.result
    });
  }

  render() {
    return (
      <div>
        {/* Iterate through keys of inventory API data */}
        {/* Managing updated state is easier with objects */}
        {Object.keys(this.state.inventory).map(uid => (
          <Item
            {...this.state.inventory[uid]}
            sendUpdate={() => {
              const data = {
                ...this.state.inventory[uid]
              };
              this.props.sendForm(this.props.API_URL, 'PATCH', data);
            }}
            sendDelete={() => {
              const data = {
                ...this.state.inventory[uid]
              };
              this.props.sendForm(this.props.API_URL, 'DELETE', data);
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

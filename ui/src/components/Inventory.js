import React, { Component } from 'react';

export default class Inventory extends Component {
  render() {
    return (
      <div>
        {this.props.inventory.map(item => (
          <div>
            <span>
              <button>
                +
              </button>
              <button>
                -
              </button>
              <button>
                Delete
              </button>
            </span>
            <span>
              <b>{item.item_name}</b>: {item.quantity}
            </span>
          </div>
        ))}
      </div>
    );
  };
}

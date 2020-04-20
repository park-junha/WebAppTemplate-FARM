import React, { Component } from 'react';

export default class Item extends Component {
  render() {
    return (
      <div>
        <span>
          <input
            type='button'
            onClick={() => {this.props.incrementItem()}}
            value='+'
          />
          <input
            type='button'
            onClick={() => {this.props.decrementItem()}}
            value='-'
          />
          <input
            type='button'
            onClick={() => {this.props.sendUpdate()}}
            value='Update'
          />
          <input
            type='button'
            onClick={() => {this.props.sendDelete()}}
            value='Delete'
          />
        </span>
        <span>
          <b>{this.props.item_name}</b>: {this.props.quantity}
        </span>
      </div>
    );
  };
}

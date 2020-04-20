import React, { Component } from 'react';

export default class Item extends Component {
  constructor(props) {
    super(props);
    this.state = {
      itemState: 'item-no-state',
    };
  }

  render() {
    return (
      <div>
        <span>
          <input
            type='button'
            onClick={() => {
              this.props.incrementItem();
              this.setState({
                itemState: 'item-state-edited',
              });
            }}
            disabled={this.state.itemState === 'item-state-deleted' ? true : false}
            value='+'
          />
          <input
            type='button'
            onClick={() => {
              this.props.decrementItem();
              this.setState({
                itemState: 'item-state-edited',
              });
            }}
            disabled={this.state.itemState === 'item-state-deleted' ? true : false}
            value='-'
          />
          <input
            type='button'
            onClick={async () => {
              this.setState({
                itemState: await this.props.sendUpdate(),
              });
            }}
            disabled={this.state.itemState === 'item-state-deleted' ? true : false}
            value='Update'
          />
          <input
            type='button'
            onClick={async () => {
              this.setState({
                itemState: await this.props.sendDelete(),
              });
            }}
            disabled={this.state.itemState === 'item-state-deleted' ? true : false}
            value='Delete'
          />
        </span>
        <span>
          <b>
            {this.props.item_name}
          </b>: <span className={this.state.itemState}>
            {this.props.quantity}
          </span>
        </span>
      </div>
    );
  };
}

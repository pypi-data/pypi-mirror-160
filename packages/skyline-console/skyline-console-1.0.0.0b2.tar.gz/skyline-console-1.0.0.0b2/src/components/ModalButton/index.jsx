// Copyright 2021 99cloud
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

import React, { Component } from 'react';
import { Modal, Button } from 'antd';
import PropTypes from 'prop-types';
import { generateId } from 'utils/index';

export default class ModalButton extends Component {
  static propTypes() {
    return {
      title: PropTypes.string.isRequired,
      buttonType: PropTypes.string,
      render: PropTypes.func,
      component: PropTypes.node,
      item: PropTypes.any,
      modalSize: PropTypes.string,
      okText: PropTypes.string,
      cancelText: PropTypes.string,
      handleOk: PropTypes.func,
      className: PropTypes.func,
      buttonText: PropTypes.string,
      buttonClassName: PropTypes.string,
      showCancelButton: PropTypes.bool,
      style: PropTypes.object,
      onClickButton: PropTypes.func,
      onFinishAction: PropTypes.func,
      onCancelAction: PropTypes.func,
    };
  }

  static defaultProps = {
    buttonType: 'primary',
    render: null,
    component: null,
    item: null,
    okText: t('Confirm'),
    cancelText: t('Cancel'),
    handleOk: null,
    className: '',
    buttonClassName: '',
    showCancelButton: false,
    style: {},
    onClickButton: null,
    onFinishAction: null,
    onCancelAction: null,
  };

  constructor(props) {
    super(props);
    this.state = {
      visible: false,
      submitLoading: false,
    };
  }

  getModalWidth = (size) => {
    switch (size) {
      case 'small':
        return 520;
      case 'middle':
        return 720;
      case 'large':
        return 1200;
      default:
        return 520;
    }
  };

  onClick = (e) => {
    e && e.stopPropagation();
    const { onClickButton } = this.props;
    onClickButton && onClickButton();
    this.showModal();
  };

  onFinishAction = () => {
    const { onFinishAction } = this.props;
    onFinishAction && onFinishAction();
  };

  handleOk = () => {
    const { handleOk } = this.props;
    if (handleOk) {
      this.setState({
        submitLoading: true,
      });
      const result = handleOk();
      if (result instanceof Promise) {
        handleOk().finally(() => {
          this.hideModal();
          this.onFinishAction();
          this.setState({
            submitLoading: false,
          });
        });
      } else {
        this.hideModal();
        this.onFinishAction();
        this.setState({
          submitLoading: false,
        });
      }
    } else {
      this.hideModal();
      this.onFinishAction();
    }
  };

  handleCancel = () => {
    const { onCancelAction } = this.props;
    onCancelAction && onCancelAction();
    this.hideModal();
  };

  hideModal = () => {
    this.setState({
      visible: false,
    });
  };

  showModal = () => {
    this.setState({
      visible: true,
    });
  };

  renderModal() {
    const { visible, submitLoading } = this.state;
    if (!visible) {
      return null;
    }
    const {
      title,
      item,
      modalSize,
      className,
      okText,
      cancelText,
      render,
      component,
      showCancelButton,
    } = this.props;
    const width = this.getModalWidth(modalSize);
    const content = render ? render(item) : component;
    const configs = {
      visible,
      title,
      key: `modal-${generateId()}`,
      className,
      width,
      onOk: this.handleOk,
      onCancel: this.handleCancel,
      okText,
      cancelText,
      confirmLoading: submitLoading,
    };
    if (!showCancelButton) {
      configs.cancelButtonProps = {
        style: { display: 'none' },
      };
    }
    return <Modal {...configs}>{content}</Modal>;
  }

  render() {
    const { buttonText, title, danger, style, buttonType, buttonClassName } =
      this.props;
    return (
      <>
        <Button
          type={buttonType}
          danger={danger}
          onClick={this.onClick}
          className={buttonClassName}
          style={style}
        >
          {buttonText || title}
        </Button>
        {this.renderModal()}
      </>
    );
  }
}

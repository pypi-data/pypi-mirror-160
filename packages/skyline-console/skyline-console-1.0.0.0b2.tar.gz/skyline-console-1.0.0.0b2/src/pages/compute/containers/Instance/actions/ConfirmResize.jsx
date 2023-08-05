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

import { ConfirmAction } from 'containers/Action';
import globalServerStore from 'stores/nova/instance';

export default class ConfirmResizeAction extends ConfirmAction {
  get id() {
    return 'confirm_resize_migrate';
  }

  get title() {
    return t('Confirm Resize or Migrate');
  }

  get buttonText() {
    return t('Confirm Resize or Migrate');
  }

  get actionName() {
    return t('confirm resize or migrate');
  }

  policy = 'os_compute_api:servers:resize';

  allowedCheckFunc = (item) => {
    if (!item) {
      return true;
    }
    return item.status.toLowerCase() === 'verify_resize';
  };

  confirmContext = (data) => {
    const name = this.getName(data);
    return t(`${this.actionNameDisplay} (instance: {name})?`, {
      name,
    });
  };

  onSubmit = (item) => {
    const { id } = item || this.item;
    return globalServerStore.update(id, {
      confirmResize: null,
    });
  };
}

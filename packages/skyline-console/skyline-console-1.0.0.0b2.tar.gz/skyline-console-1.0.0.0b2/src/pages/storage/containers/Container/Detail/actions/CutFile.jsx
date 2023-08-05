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
import globalObjectStore from 'stores/swift/object';
import { allCanChangePolicy } from 'resources/skyline/policy';
import { isFile } from 'resources/swift/container';

export default class CutFile extends ConfirmAction {
  get id() {
    return 'CutFile';
  }

  get title() {
    return t('Cut File');
  }

  get name() {
    return this.title;
  }

  get buttonText() {
    return t('Cut');
  }

  get actionName() {
    return this.title;
  }

  get passiveAction() {
    return t('be cut');
  }

  getItemName = (item) => item.shortName;

  policy = allCanChangePolicy;

  allowedCheckFunc = (item) => isFile(item);

  onSubmit = (value, containerProps, isBatch, index, values) => {
    if (!isBatch) {
      return globalObjectStore.cutFiles([value]);
    }
    if (index === 0) {
      return globalObjectStore.cutFiles(values);
    }
    return Promise.resolve();
  };
}

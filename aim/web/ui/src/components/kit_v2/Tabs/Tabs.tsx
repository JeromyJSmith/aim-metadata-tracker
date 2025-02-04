import React, { Suspense } from 'react';

import { TabContent, TabList, TabRoot, TabTrigger } from './Tabs.style';
import { ITabsProps } from './Tabs.d';

/**
 * @description - Tabs component of the kit
 * @param {ITabsProps} props - props of the component
 * @param {ITab[]} props.tabs - array of tabs
 * @param {string} props.orientation - vertical or horizontal
 * @param {string} props.defaultValue - default value of the tab
 * @returns
 */
const Tabs = ({
  tabs,
  orientation = 'horizontal',
  defaultValue,
  ...props
}: ITabsProps) => (
  <TabRoot
    {...props}
    className='TabRoot'
    defaultValue={defaultValue || tabs[0].value}
    orientation={orientation}
  >
    <TabList className='TabList'>
      {tabs.map((tab, index: number) => (
        <TabTrigger
          data-testid={tab.value}
          disabled={tab.disabled}
          key={index}
          value={tab.value}
        >
          {tab.label}
        </TabTrigger>
      ))}
    </TabList>
    <Suspense fallback={<div>Loading...</div>}>
      {tabs.map((tab, index: number) => {
        return (
          <TabContent className='TabContent' key={index} value={tab.value}>
            {tab.content}
          </TabContent>
        );
      })}
    </Suspense>
  </TabRoot>
);

export default React.memo(Tabs);

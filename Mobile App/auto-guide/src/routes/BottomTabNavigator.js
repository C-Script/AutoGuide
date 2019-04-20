import { createMaterialTopTabNavigator } from 'react-navigation';
import Icon from 'react-native-vector-icons/FontAwesome';
import React from 'react';

import { colors, sizes } from '../assets/styles/base';
import CaptureScreen from '../screens/TabScreens/Capture';
import InfoScreen from '../screens/TabScreens/Info';

export default createMaterialTopTabNavigator(
  {
    Capture: {
      screen: CaptureScreen,
      // --specific navigationOptions for each tab
      navigationOptions: {
        tabBarLabel: 'Capture',
        tabBarIcon: () => (
          <Icon name="camera-retro" size={24} color={colors.secondary} />
        ),
      },
    },
    Info: {
      screen: InfoScreen,
      navigationOptions: {
        tabBarLabel: 'Info',
        tabBarIcon: () => (
          <Icon name="book" size={24} color={colors.secondary} />
        ),
      },
    },
  },
  {
    // Config

    initialRouteName: 'Capture',
    order: ['Capture', 'Info'],
    tabBarPosition: 'bottom',
    swipeEnabled: true,
    animationEnabled: false,

    tabBarOptions: {
      showIcon: true,
      upperCaseLabel: false,
      activeTintColor: colors.secondary,
      inactiveTintColor: colors.secondary,

      style: {
        backgroundColor: colors.primary,
        height: sizes.bottomTabHeight,
        borderTopWidth: 0.5,
        borderTopColor: '#00000000',
      },
      labelStyle: {},
      iconStyle: {},
      indicatorStyle: {
        backgroundColor: colors.secondary,
      },
    },
  },
);

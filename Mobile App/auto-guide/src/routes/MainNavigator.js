import { createStackNavigator, createAppContainer } from 'react-navigation';

import { colors } from '../assets/styles/base';
import BottomTabNavigator from './BottomTabNavigator';

const RootNavigator = createStackNavigator(
  {
    Tab: BottomTabNavigator,
  },
  {
    initialRouteName: 'Tab',

    // We only need to configure the header options only for the 'tab' screens here
    // But for other screens, we do that in their own components

    defaultNavigationOptions: ({ navigation }) => {
      // --first, we check which screen it is:
      const screen = navigation.state.routeName;

      // values we will modify then return:
      let headerTitle = '';
      const headerRight = '';
      const headerLeft = '';
      let headerStyle = {
        backgroundColor: colors.primary,
      };
      const headerTitleStyle = {
        color: colors.white,
      };
      const tabBarVisible = true;
      // and so on...

      // For each screen:
      if (screen === 'Tab') {
        const { routes, index } = navigation.state;
        const tabScreen = routes[index].routeName;

        // Capture tab screen
        if (tabScreen === 'Capture') {
          headerTitle = 'Capture a statue picture! 🇪🇬';
          headerStyle = {
            backgroundColor: colors.primary,
          };
        }

        // Info tab screen
        if (tabScreen === 'Info') {
          headerTitle = 'Info 📜';
          headerStyle = {
            backgroundColor: colors.primary,
          };
        }

        // Return these in case of tab screens
        return {
          tabBarVisible,
          headerStyle,
          headerTitle,
          headerRight,
          headerLeft,
          headerTitleStyle,
          // and so on..
        };
      }

      // Return these for other screens (could just return {})
      return {
        headerStyle,
        headerTitleStyle,
      };
    },
  },
);

export default createAppContainer(RootNavigator);

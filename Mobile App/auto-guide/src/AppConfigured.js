import React, { Component } from 'react';

import { loadFonts } from './assets/fonts/loadFonts';
import LoadingScreen from './screens/common/LoadingScreen';
import MainNavigator from './routes/MainNavigator';

// This is the main app, with these configured:
// 1- Customized fonts loaded

class AppConfigured extends Component {
  state = {
    fontLoaded: false,
  };

  componentDidMount() {
    this.loadAssetsAsync();
  }

  async loadAssetsAsync() {
    await Promise.all(loadFonts);

    this.setState(() => ({ fontLoaded: true }));
  }

  render() {
    const { fontLoaded } = this.state;

    if (!fontLoaded) {
      return <LoadingScreen />;
    }

    return <MainNavigator />;
  }
}

AppConfigured.propTypes = {};

export default AppConfigured;

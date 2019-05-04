import {
  View, Image, Text, ScrollView,
} from 'react-native';
import PropTypes from 'prop-types';
import React, { Component } from 'react';

import { dimensions } from '../../../assets/styles/base';
import allInfo from '../../../assets/info';
import SnakeNavigator from '../../../components/snakeNavigator';
import styles from './styles';

class InfoScreen extends Component {
  state = {
    imageUri: '',
    imageInfo: '',
  };

  componentWillReceiveProps(nextProps) {
    const { navigation } = this.props;
    const { navigation: nextNavigation } = nextProps;
    if (nextNavigation.state.params !== navigation.state.params) {
      this.setState({
        imageUri: nextNavigation.state.params.imageUri,
        imageInfo: allInfo.find(
          oneInfo => oneInfo.name === nextNavigation.state.params.imageName,
        ),
      });
    }
  }

  getSnakeNavigatorContent = () => {
    const { imageInfo } = this.state;
    return [
      {
        name: 'بالعربية',
        component: () => (
          <Text style={styles.info}>{imageInfo.info_in_arabic}</Text>
        ),
      },
      {
        name: 'In English',
        component: () => (
          <Text style={styles.info}>{imageInfo.info_in_english}</Text>
        ),
      },
    ];
  };

  render() {
    const { imageUri, imageInfo } = this.state;
    const { navigation } = this.props;

    return (
      <ScrollView contentContainerStyle={styles.container}>
        {imageUri ? (
          <View>
            <Text style={styles.infoTitle}>{imageInfo.name}</Text>

            <Image
              source={{
                uri: imageUri,
              }}
              style={styles.image}
            />
            <SnakeNavigator
              content={this.getSnakeNavigatorContent()}
              navigation={navigation}
              snakeWidth={dimensions.fullWidth * 0.7}
            />
          </View>
        ) : (
          <Text style={styles.notCaptured}>
            {'You haven\'t captured any image yet'}
          </Text>
        )}
      </ScrollView>
    );
  }
}

InfoScreen.defaultProps = {
  navigation: {},
};

InfoScreen.propTypes = {
  navigation: PropTypes.shape({}),
};

export default InfoScreen;

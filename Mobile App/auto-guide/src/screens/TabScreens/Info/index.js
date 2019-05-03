import { View, Image, Text, ScrollView } from 'react-native';
import PropTypes from 'prop-types';
import React, { Component } from 'react';
import info from '../../../assets/info';
import { dimensions } from '../../../assets/styles/base';
import styles from './styles';
import SnakeNavigator from '../../../components/snakeNavigator';

class InfoScreen extends Component {
  state = {
    imageUri: '',
  };

  componentWillReceiveProps(nextProps) {
    if (nextProps.navigation.state.params !== this.props.navigation.state.params) {
      this.setState({ imageUri: nextProps.navigation.state.params.imageUri });
    }
  }

  getSnakeNavigatorContent = () => {
    return [
      {
        name: 'Info In Arabic',
        component: () => (
          <Text style={styles.info}>{info[0].info_in_arabic}</Text>
        ),
      },
      {
        name: 'Info In English',
        component: () => (
          <Text style={styles.info}>{info[0].info_in_english}</Text>
        ),
      },
    ];
  };

  render() {
    const { imageUri } = this.state;
    const { navigation } = this.props;


    return (
      <ScrollView contentContainerStyle={styles.container}>
        {imageUri ? (
          <View>
            <Text style={styles.infoTitle}>{info[0].name}</Text>

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
            {"You haven't captured any image yet"}
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

import { StyleSheet } from 'react-native';
import { colors } from '../../../assets/styles/base';

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.white,
    alignItems: 'center',
    justifyContent: 'center',
  },
  image: {
    width: 200,
    height: 330,
    borderRadius: 10,
    borderWidth: 3,
    borderColor: colors.white,
  },
});

export default styles;

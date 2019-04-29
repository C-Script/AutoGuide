import { StyleSheet } from 'react-native';
import { colors } from '../../../assets/styles/base';

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.white,
    alignItems: 'center',
    justifyContent: 'center',
  },
  button: {
    borderRadius: 50,
    backgroundColor: colors.secondary,
    padding: 15,
    width: '90%',
  },
  buttonText: {
    fontSize: 20,
    color: colors.white,
    textAlign: 'center',
  },
  separatorText:{margin:5}
});

export default styles;

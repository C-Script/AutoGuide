import { Permissions } from 'expo';

export const ensureCameraPermission = async (callback) => {
  const { status: existingStatus } = await Permissions.getAsync(
    Permissions.CAMERA,
  );

  if (existingStatus !== 'granted') {
    await Permissions.askAsync(Permissions.CAMERA);
  }

  if (callback) callback();
};

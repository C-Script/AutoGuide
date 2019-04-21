import { Permissions } from 'expo';

export const ensureCameraPermission = async (callback) => {
  // Camera Permission
  const { status: cameraStatus } = await Permissions.getAsync(
    Permissions.CAMERA,
  );
  if (cameraStatus !== 'granted') {
    await Permissions.askAsync(Permissions.CAMERA);
  }

  // Camera Roll Permission
  const { status: cameraRollStatus } = await Permissions.getAsync(
    Permissions.CAMERA_ROLL,
  );
  if (cameraRollStatus !== 'granted') {
    await Permissions.askAsync(Permissions.CAMERA_ROLL);
  }

  if (cameraStatus === 'granted' && cameraRollStatus === 'granted') {
    if (callback) callback();
  }
};

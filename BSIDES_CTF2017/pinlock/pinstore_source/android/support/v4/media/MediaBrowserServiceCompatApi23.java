package android.support.v4.media;

import android.media.browse.MediaBrowser.MediaItem;
import android.os.Bundle;
import android.os.Parcel;
import android.os.ResultReceiver;
import android.service.media.MediaBrowserService;
import android.support.v4.media.MediaBrowserServiceCompatApi21.ServiceImplApi21;
import android.util.Log;

class MediaBrowserServiceCompatApi23 extends MediaBrowserServiceCompatApi21 {
    private static final String TAG = "MediaBrowserServiceCompatApi21";

    public interface ItemCallback {
        void onItemLoaded(int i, Bundle bundle, Parcel parcel);
    }

    static class MediaBrowserServiceAdaptorApi23 extends MediaBrowserServiceAdaptorApi21 {

        private static class ServiceBinderProxyApi23 extends ServiceBinderProxyApi21 {
            ServiceImplApi23 mServiceImpl;

            /* renamed from: android.support.v4.media.MediaBrowserServiceCompatApi23.MediaBrowserServiceAdaptorApi23.ServiceBinderProxyApi23.1 */
            class C01861 implements ItemCallback {
                final /* synthetic */ String val$KEY_MEDIA_ITEM;
                final /* synthetic */ ResultReceiver val$receiver;

                C01861(String str, ResultReceiver resultReceiver) {
                    this.val$KEY_MEDIA_ITEM = str;
                    this.val$receiver = resultReceiver;
                }

                public void onItemLoaded(int resultCode, Bundle resultData, Parcel itemParcel) {
                    if (itemParcel != null) {
                        itemParcel.setDataPosition(0);
                        resultData.putParcelable(this.val$KEY_MEDIA_ITEM, (MediaItem) MediaItem.CREATOR.createFromParcel(itemParcel));
                        itemParcel.recycle();
                    }
                    this.val$receiver.send(resultCode, resultData);
                }
            }

            ServiceBinderProxyApi23(ServiceImplApi23 serviceImpl) {
                super(serviceImpl);
                this.mServiceImpl = serviceImpl;
            }

            public void getMediaItem(String mediaId, ResultReceiver receiver) {
                ReflectiveOperationException e;
                try {
                    this.mServiceImpl.getMediaItem(mediaId, new C01861((String) MediaBrowserService.class.getDeclaredField("KEY_MEDIA_ITEM").get(null), receiver));
                } catch (IllegalAccessException e2) {
                    e = e2;
                    Log.i(MediaBrowserServiceCompatApi23.TAG, "Failed to get KEY_MEDIA_ITEM via reflection", e);
                } catch (NoSuchFieldException e3) {
                    e = e3;
                    Log.i(MediaBrowserServiceCompatApi23.TAG, "Failed to get KEY_MEDIA_ITEM via reflection", e);
                }
            }
        }

        MediaBrowserServiceAdaptorApi23() {
        }

        public void onCreate(ServiceImplApi23 serviceImpl) {
            this.mBinder = new ServiceBinderProxyApi23(serviceImpl);
        }
    }

    public interface ServiceImplApi23 extends ServiceImplApi21 {
        void getMediaItem(String str, ItemCallback itemCallback);
    }

    MediaBrowserServiceCompatApi23() {
    }

    public static Object createService() {
        return new MediaBrowserServiceAdaptorApi23();
    }

    public static void onCreate(Object serviceObj, ServiceImplApi23 serviceImpl) {
        ((MediaBrowserServiceAdaptorApi23) serviceObj).onCreate(serviceImpl);
    }
}

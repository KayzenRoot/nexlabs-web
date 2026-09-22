import Image from "next/image";
import { contextCoreStaticFallbacks } from "@/three/core/contextCoreAssets";

export function StaticContextCore() {
  return (
    <div className="context-core-static" aria-hidden="true">
      <picture className="context-core-static-picture context-core-static-landscape">
        <source type="image/avif" srcSet={contextCoreStaticFallbacks.landscape.avifUrl} />
        <source type="image/webp" srcSet={contextCoreStaticFallbacks.landscape.webpUrl} />
        <Image className="context-core-static-image" src={contextCoreStaticFallbacks.landscape.url} alt="" fill sizes="(max-width: 48rem) 100vw, 45vw" priority unoptimized />
      </picture>
      <picture className="context-core-static-picture context-core-static-portrait">
        <source type="image/avif" srcSet={contextCoreStaticFallbacks.portrait.avifUrl} />
        <source type="image/webp" srcSet={contextCoreStaticFallbacks.portrait.webpUrl} />
        <Image className="context-core-static-image" src={contextCoreStaticFallbacks.portrait.url} alt="" fill sizes="100vw" unoptimized />
      </picture>
      <picture className="context-core-static-picture context-core-static-square">
        <source type="image/avif" srcSet={contextCoreStaticFallbacks.square.avifUrl} />
        <source type="image/webp" srcSet={contextCoreStaticFallbacks.square.webpUrl} />
        <Image className="context-core-static-image" src={contextCoreStaticFallbacks.square.url} alt="" fill sizes="100vw" unoptimized />
      </picture>
      <span className="context-core-static-wash" />
    </div>
  );
}

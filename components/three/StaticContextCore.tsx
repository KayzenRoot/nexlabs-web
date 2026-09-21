import Image from "next/image";
import { contextCoreStaticFallbacks } from "@/three/core/contextCoreAssets";

export function StaticContextCore() {
  return (
    <div className="context-core-static" aria-hidden="true">
      <Image className="context-core-static-image context-core-static-landscape" src={contextCoreStaticFallbacks.landscape.url} alt="" fill sizes="(max-width: 48rem) 100vw, 45vw" priority />
      <Image className="context-core-static-image context-core-static-portrait" src={contextCoreStaticFallbacks.portrait.url} alt="" fill sizes="100vw" />
      <Image className="context-core-static-image context-core-static-square" src={contextCoreStaticFallbacks.square.url} alt="" fill sizes="100vw" />
      <span className="context-core-static-wash" />
    </div>
  );
}

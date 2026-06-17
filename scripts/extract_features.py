import cv2
import numpy as np

def analyze_image(name, vis_path, ir_path):
    vis = cv2.imread(vis_path, cv2.IMREAD_GRAYSCALE)
    ir = cv2.imread(ir_path)
    b, g, r = cv2.split(ir)
    
    # Let's define some zones manually based on brightness to see what they are
    # Ocean: Dark visible, Warm IR (High Blue)
    ocean_mask = (vis < 50) & (b > 100)
    print(f"[{name}] OCEAN  -> Vis: {vis[ocean_mask].mean():.0f}, R: {r[ocean_mask].mean():.0f}, G: {g[ocean_mask].mean():.0f}, B: {b[ocean_mask].mean():.0f}")
    
    # Storm: Bright visible, Cold IR (High Red, Low Green)
    storm_mask = (vis > 150) & (r > 150) & (g < 100)
    print(f"[{name}] STORM  -> Vis: {vis[storm_mask].mean():.0f}, R: {r[storm_mask].mean():.0f}, G: {g[storm_mask].mean():.0f}, B: {b[storm_mask].mean():.0f}")
    
    # Desert/Warm Land: High Green, High Red, Low Blue
    desert_mask = (g > 100) & (r > 100) & (b < 100)
    print(f"[{name}] DESERT -> Vis: {vis[desert_mask].mean():.0f}, R: {r[desert_mask].mean():.0f}, G: {g[desert_mask].mean():.0f}, B: {b[desert_mask].mean():.0f}")
    
    # Low Cloud: Bright visible, High Green/Blue/Red
    lowcloud_mask = (vis > 130) & (g > 100) & (b > 80)
    print(f"[{name}] LOWCLD -> Vis: {vis[lowcloud_mask].mean():.0f}, R: {r[lowcloud_mask].mean():.0f}, G: {g[lowcloud_mask].mean():.0f}, B: {b[lowcloud_mask].mean():.0f}")
    
    print("-" * 50)

demo_dir = 'backend/data/ejemplos_demostracion'
analyze_image('HURACAN', f'{demo_dir}/1_huracan_vis.jpg', f'{demo_dir}/1_huracan_ir.jpg')
analyze_image('DESIERTO', f'{demo_dir}/4_desierto_despejado_vis.jpg', f'{demo_dir}/4_desierto_despejado_ir.jpg')
analyze_image('TARAPACA', f'{demo_dir}/6_tarapaca_camanchaca_vis.jpg', f'{demo_dir}/6_tarapaca_camanchaca_ir.jpg')
analyze_image('ESTRATOS', f'{demo_dir}/5_estratocumulos_vis.jpg', f'{demo_dir}/5_estratocumulos_ir.jpg')

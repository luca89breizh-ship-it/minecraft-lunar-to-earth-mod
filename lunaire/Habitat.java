package fr.lunaire.fabric;

import java.util.ArrayDeque;
import java.util.HashSet;
import java.util.Set;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.state.BlockState;

/** Détection d'une pièce étanche : un Scelleur d'atmosphère proche + volume fermé (≤ 900 blocs d'air). */
public final class Habitat {
    private static final int LIMIT = 900;
    private Habitat() {}

    public static boolean hasSealerNear(Level level, BlockPos center, int r) {
        BlockPos.MutableBlockPos p = new BlockPos.MutableBlockPos();
        for (int dx = -r; dx <= r; dx++) {
            for (int dy = -r; dy <= r; dy++) {
                for (int dz = -r; dz <= r; dz++) {
                    p.set(center.getX() + dx, center.getY() + dy, center.getZ() + dz);
                    if (level.getBlockState(p).is(fr.lunaire.fabric.content.ModBlocks.ATMOSPHERE_SEALER)) {
                        return true;
                    }
                }
            }
        }
        return false;
    }

    /** Taille du volume fermé contenant ce point, ou -1 s'il fuit. */
    public static int enclosedVolume(Level level, BlockPos start) {
        Set<Long> seen = new HashSet<>();
        ArrayDeque<BlockPos> queue = new ArrayDeque<>();
        queue.add(start);
        seen.add(start.asLong());
        while (!queue.isEmpty()) {
            BlockPos cur = queue.poll();
            for (Direction d : Direction.values()) {
                BlockPos n = cur.relative(d);
                if (!seen.add(n.asLong())) {
                    continue;
                }
                BlockState st = level.getBlockState(n);
                if (!st.getCollisionShape(level, n).isEmpty()) {
                    continue; // mur
                }
                if (seen.size() > LIMIT) {
                    return -1;
                }
                queue.add(n);
            }
        }
        return seen.size();
    }

    public static boolean isPressurized(Level level, BlockPos pos) {
        return hasSealerNear(level, pos, 10) && enclosedVolume(level, pos) > 0;
    }
}

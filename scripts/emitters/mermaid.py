"""Mermaid class-diagram emitter."""

from pathlib import Path

from linkml_runtime.utils.schemaview import SchemaView

LAYERS = ["core", "epidemiology", "formulary", "ethnobotany"]


def _layer_for_class(sv: SchemaView, class_name: str) -> str:
    """Map a class to its schema layer."""
    c = sv.get_class(class_name)
    subsets = getattr(c, "in_subset", None) or []
    for subset in subsets:
        if subset in LAYERS:
            return subset  # type: ignore[no-any-return]
    return "core"


def emit_mermaid(schema_path: Path, output_dir: Path) -> None:
    """Write Mermaid class diagrams, one per layer."""
    sv = SchemaView(str(schema_path))
    output_dir.mkdir(parents=True, exist_ok=True)

    layer_classes: dict[str, list[str]] = {layer: [] for layer in LAYERS}
    for class_name in sv.all_classes():
        layer = _layer_for_class(sv, class_name)
        if layer not in layer_classes:
            layer = "core"
        layer_classes[layer].append(class_name)

    for layer in LAYERS:
        lines: list[str] = [
            "---",
            f"title: {layer} layer class diagram",
            "---",
            "classDiagram",
        ]
        classes = sorted(layer_classes[layer])
        # Emit class boxes
        for class_name in classes:
            c = sv.get_class(class_name)
            slots = sv.class_slots(class_name) or []
            if slots:
                lines.append(f"    class {class_name} {{")
                for slot_name in slots:
                    slot = sv.induced_slot(slot_name, class_name)
                    range_cls = getattr(slot, "range", None) or "string"
                    mult = "*" if getattr(slot, "multivalued", False) else ""
                    lines.append(f"        +{range_cls}{mult} {slot_name}")
                lines.append("    }")
            else:
                lines.append(f"    class {class_name}")
        # Emit associations
        for class_name in classes:
            for slot_name in (sv.class_slots(class_name) or []):
                slot = sv.induced_slot(slot_name, class_name)
                range_cls = getattr(slot, "range", None)
                if range_cls and range_cls in sv.all_classes():
                    lines.append(f"    {class_name} --> {range_cls} : {slot_name}")
        # Emit inheritance
        for class_name in classes:
            c = sv.get_class(class_name)
            parent = getattr(c, "is_a", None)
            if parent and parent in sv.all_classes():
                lines.append(f"    {parent} <|-- {class_name}")
        lines.append("")
        (output_dir / f"{layer}.mmd").write_text("\n".join(lines))
